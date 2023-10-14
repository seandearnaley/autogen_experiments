"""Perplexity API."""
import json
import os
from typing import Dict

import requests

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {PERPLEXITY_API_KEY}",
}


def create_payload(message: str) -> Dict:
    """Create payload."""
    return {
        "model": "llama-2-70b-chat",
        "messages": [
            {
                "role": "system",
                "content": "respond with just valid folder lower case folder names, nothing else",  # noqa: E501 pylint: disable=line-too-long
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        "max_tokens": 0,
        "temperature": 1,
        "top_p": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
    }


def ask_perplexity(message: str) -> str:
    """Ask perplexity."""
    payload = create_payload(message)
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        # Handle error response codes
        return f"Error: Received status code {response.status_code}"

    response_json = json.loads(response.text)
    content = response_json.get("choices", [{}])[0].get("message", {}).get("content")

    if content is None:
        return "Error: Content field not found in the response."

    return content


if __name__ == "__main__":
    with open("app/test.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print(ask_perplexity(text))
