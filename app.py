import os
import streamlit as st
from datetime import datetime
from utils import ensure_data_dirs, sanitize_filename, timestamp, get_project_root
from speech_to_text import transcribe_audio
from summarizer import generate_notes
from quiz_generator import generate_quiz

# ==================== INITIALIZATION ====================
ensure_data_dirs()

if "groq_api_key_active" not in st.session_state:
    st.session_state.groq_api_key_active = None
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="Lecture Voice-to-Notes", layout="wide")
st.title("Lecture Voice-to-Notes Generator")
st.write(
    "Upload a lecture audio or video file. "
    "The app transcribes it, generates study notes, and creates a quiz."
)

# ==================== SIDEBAR ====================
st.sidebar.markdown("### Configuration")

if st.session_state.groq_api_key_active:
    st.sidebar.success("🟢 AI Enabled")
else:
    st.sidebar.error("🔴 AI Disabled")

groq_api_key_input = st.sidebar.text_input(
    "Groq API Key (starts with gsk_)",
    type="password"
)

st.sidebar.link_button(
    "🔑 Get Free Groq API Key",
    "https://console.groq.com/keys",
    use_container_width=True
)

if st.sidebar.button("✅ Enable AI", use_container_width=True):
    if not groq_api_key_input:
        st.sidebar.error("API key cannot be empty.")
    elif not groq_api_key_input.startswith("gsk_"):
        st.sidebar.error("Invalid API key format.")
    else:
        st.session_state.groq_api_key_active = groq_api_key_input
        st.sidebar.success("AI enabled successfully.")
        st.rerun()

if not st.session_state.groq_api_key_active:
    st.sidebar.warning("Enter API key and click Enable AI.")

# ==================== FILE UPLOAD ====================
uploaded_file = st.file_uploader(
    "Upload lecture audio or video",
    type=["mp3", "wav", "m4a", "mp4", "avi", "mov", "mkv"]
)

if uploaded_file:
    project_root = get_project_root()
    audio_dir = os.path.join(project_root, "data", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    base = sanitize_filename(uploaded_file.name)
    out_file = f"{base}_{timestamp()}{os.path.splitext(uploaded_file.name)[1]}"
    out_path = os.path.join(audio_dir, out_file)

    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.uploaded_file_path = out_path

    # ==================== TRANSCRIPTION ====================
    if st.session_state.transcript is None:
        with st.spinner("Transcribing audio with Whisper..."):
            st.session_state.transcript = transcribe_audio(out_path)
            st.session_state.summary = None
            st.session_state.quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False

    # ==================== TRANSCRIPT ====================
    st.subheader("Transcript")
    st.text(st.session_state.transcript)

    st.download_button(
        "⬇ Download Transcript",
        st.session_state.transcript,
        file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

    # ==================== NOTES ====================
    if st.button("📝 Generate Notes"):
        if not st.session_state.groq_api_key_active:
            st.error("Enable AI first.")
        else:
            with st.spinner("Generating notes..."):
                st.session_state.summary = generate_notes(
                    st.session_state.groq_api_key_active,
                    st.session_state.transcript
                )

    if st.session_state.summary:
        st.subheader("📚 Study Notes")
        st.markdown(st.session_state.summary)

        st.download_button(
            "⬇ Download Summary",
            st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain"
        )

    # ==================== QUIZ ====================
    if st.button("📋 Generate Quiz"):
        if not st.session_state.groq_api_key_active:
            st.error("Enable AI first.")
        else:
            with st.spinner("Generating quiz..."):
                st.session_state.quiz = generate_quiz(
                    st.session_state.groq_api_key_active,
                    st.session_state.transcript
                )
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False

    # ==================== INTERACTIVE QUIZ ====================
    if st.session_state.quiz:
        st.subheader("📝 Quiz")

        for i, q in enumerate(st.session_state.quiz, start=1):
            question = q["question"]
            options = q["options"]
            correct = q["correct_answer"]

            st.markdown(f"**Q{i}. {question}**")

            choice = st.radio(
                "Select an option",
                ["A", "B", "C", "D"],
                index=None,
                key=f"q_{i}",
                format_func=lambda x: f"{x}. {options[ord(x)-65]}",
                label_visibility="collapsed"
            )

            st.session_state.quiz_answers[i] = choice

            if st.session_state.quiz_submitted:
                if choice is None:
                    st.warning("Not answered.")
                    st.info(f"Correct: {correct}. {options[ord(correct)-65]}")
                elif choice == correct:
                    st.success(f"Correct: {correct}. {options[ord(correct)-65]}")
                else:
                    st.error(f"Wrong: {choice}. {options[ord(choice)-65]}")
                    st.info(f"Correct: {correct}. {options[ord(correct)-65]}")

            st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📝 Submit Test"):
                st.session_state.quiz_submitted = True
                st.rerun()

        with col2:
            if st.button("🔄 Reset Quiz"):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

        if st.session_state.quiz_submitted:
            score = sum(
                1 for i, q in enumerate(st.session_state.quiz, start=1)
                if st.session_state.quiz_answers.get(i) == q["correct_answer"]
            )
            total = len(st.session_state.quiz)
            st.success(f"Score: {score} / {total}")
else:
    st.info("Upload a lecture file to begin.")
