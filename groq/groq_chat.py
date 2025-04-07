import requests

api_key = "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"
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def chat_with_groq(prompt):
    data = {
        "model": "mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
