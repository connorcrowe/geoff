import requests
import re

import os


llm_api = os.getenv("LLM_API_URL")

def generate_sql(prompt) -> str:
    model = "llama3.2"
    res = requests.post(
        llm_api,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    print("[DEBUG] URL:", llm_api)
    print(f"(LLM)[DEBUG] Model: {model}")
    print("[DEBUG] Status code:", res.status_code)
    print("[DEBUG] Response text:", res.text)
    raw_response = res.json()["response"]

    print(f"(LLM)[DEBUG] Raw response:\n{raw_response}")
    match = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print(f"(LLM)[DEBUG] SQL Detected and cleaned:\n{cleaned_sql}")
        return cleaned_sql

    return raw_response