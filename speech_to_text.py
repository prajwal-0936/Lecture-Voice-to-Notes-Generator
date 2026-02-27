import subprocess
from pathlib import Path
import re

# Whisper import - open-source local speech-to-text
try:
    import whisper
except Exception:
    whisper = None


def convert_video_to_audio(video_path: str) -> str:
    """
    Convert video file to MP3 audio using ffmpeg.
    """
    video_exts = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm", ".mts", ".m4a"}
    file_ext = Path(video_path).suffix.lower()

    if file_ext not in video_exts:
        return video_path

    audio_path = video_path.replace(file_ext, ".mp3")

    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-q:a", "9",
            "-n",
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0 and "File exists" not in result.stderr:
            raise RuntimeError(f"FFmpeg conversion failed: {result.stderr}")

        return audio_path

    except FileNotFoundError:
        raise RuntimeError(
            "FFmpeg not found. Install FFmpeg from https://ffmpeg.org/download.html "
            "and add it to system PATH."
        )


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio or video file using Whisper 'base' model
    and format the transcript into readable paragraphs.
    """
    if whisper is None:
        raise RuntimeError("Whisper is not installed. Install openai-whisper first.")

    # Convert video to audio if required
    file_ext = Path(audio_path).suffix.lower()
    if file_ext in {".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm", ".mts"}:
        audio_path = convert_video_to_audio(audio_path)

    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe (force English)
    result = model.transcribe(
        audio_path,
        language="en",
        verbose=False
    )

    raw_text = result.get("text", "").strip()

    # 🔹 STEP 1: Normalize whitespace
    text = re.sub(r"\s+", " ", raw_text)

    # 🔹 STEP 2: Add paragraph breaks after sentence-ending punctuation
    # This converts one-line transcript into readable paragraphs
    text = re.sub(r"([.!?])\s+", r"\1\n", text)

    return text.strip()
