import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


def generate_notes(api_key: str, transcript: str) -> str:
    """
    Generate structured study notes from a lecture transcript
    using Groq LLaMA-3.1 via REST API.
    """

    if not api_key:
        raise ValueError("Groq API key is missing.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert academic note-taking assistant. "
                    "Convert the lecture into clear, well-structured study notes "
                    "using headings and bullet points."
                )
            },
            {
                "role": "user",
                "content": transcript
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error ({response.status_code}): {response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]
