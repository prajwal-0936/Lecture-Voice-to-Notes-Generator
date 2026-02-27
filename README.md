---
title: Lecture Voice-to-Notes Generator
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
---
# 📘 Lecture Voice-to-Notes Generator

## 🎓 Project Overview
Students often miss important points during lectures because it is difficult to listen, understand, and write notes simultaneously.  
This project solves the problem by converting **lecture audio/video into text**, generating **structured study notes**, and creating an **interactive quiz** using modern AI models.

The system is designed as a **final-year major project** and demonstrates the practical application of **Speech-to-Text AI** and **Generative AI**.

---

## 🚀 Features
- 🎙 Upload lecture **audio or video** files
- 📝 Automatic **English transcription** using Whisper
- 📚 AI-generated **study notes**
- 🧠 AI-generated **MCQ quiz**
- 🧪 Interactive quiz with:
  - No default answers
  - Score calculation
  - Correct (🟢) / Incorrect (🔴) feedback
- ⬇ Download:
  - Transcript
  - Study notes
  - Quiz with answers
- 🔐 Secure **API key input via UI** (no hardcoded keys)

---

## 🛠️ Technology Stack

### Programming Language
- Python 3.9+

### Framework & Libraries
- Streamlit (User Interface)
- Whisper (Speech-to-Text)
- Groq API (LLaMA-3.1)
- FFmpeg (Audio/Video processing)

### AI Models
- **Speech-to-Text:** Whisper
- **Text Generation:** Groq LLaMA-3.1-8B-Instant

---

## 🧩 System Architecture
1. User uploads lecture audio or video
2. Audio is transcribed into English text
3. Transcript is summarized into structured study notes
4. Quiz is generated from the transcript
5. User attempts the quiz and receives a score
6. Outputs can be downloaded for offline study

---

## 🔑 API Key Configuration (Groq)

This project uses the **Groq API** for free and fast LLM inference.

### Steps:
1. Visit: https://console.groq.com/keys
2. Create a **free Groq API key**
3. Paste the key into the **sidebar input** in the application
4. Click **“Enable AI”**

⚠️ No environment variables are required  
⚠️ API keys are **never stored in the source code**

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt

## 📊 Use Cases
- College students  
- Online learners  
- Lecture revision  
- Exam preparation  
- Self-study automation  

---

## 🧠 Learning Outcomes
- Understanding Speech-to-Text systems  
- Applying Generative AI in real-world applications  
- Streamlit state management  
- Secure API handling  
- End-to-end AI system design  

---

## 🏁 Conclusion
The Lecture Voice-to-Notes Generator provides an effective solution for automated lecture understanding. By combining speech recognition and generative AI, the system improves learning efficiency and reduces manual effort for students.


