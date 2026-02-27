import requests
import json
import re

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


def _extract_json(text: str) -> dict:
    """
    Safely extract JSON object from LLM response text.
    Handles markdown, extra text, and formatting noise.
    """
    # Try direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    raise RuntimeError("LLM response did not contain valid JSON.")


def generate_quiz(api_key: str, transcript: str):
    """
    Generate a 5-question MCQ quiz from lecture transcript
    using Groq LLaMA-3.1 via REST API.
    """

    if not api_key:
        raise ValueError("Groq API key is missing.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = (
        "Create exactly 5 multiple-choice questions (MCQs).\n\n"
        "Rules:\n"
        "- Each question must have 4 options\n"
        "- Options must be concise\n"
        "- correct_answer must be one of A, B, C, or D\n"
        "- Return ONLY valid JSON (no markdown, no explanation)\n\n"
        "JSON format:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "question": "Question text",\n'
        '      "options": ["Option A", "Option B", "Option C", "Option D"],\n'
        '      "correct_answer": "A"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Lecture:\n"
        f"{transcript}"
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an exam question generator. "
                    "Follow the JSON format strictly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error ({response.status_code}): {response.text}"
        )

    content = response.json()["choices"][0]["message"]["content"]

    quiz_data = _extract_json(content)

    if "questions" not in quiz_data:
        raise RuntimeError("Quiz JSON missing 'questions' field.")

    return quiz_data["questions"]
