import requests
import re

import os

#OLLAMA_API_URL = os.getenv("LLM_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

def generate_sql(prompt) -> str:
    """
    Generates SQL from a user/system prompt using OpenAI Chat Completions API.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a SQL expert who generates PostGIS queries."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,  
        "max_tokens": 1024
    }

    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    res.raise_for_status()
    raw_response = res.json()["choices"][0]["message"]["content"]

    # model = "llama3.2"
    # res = requests.post(
    #     OLLAMA_API_URL,
    #     json={
    #         "model": model,
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )
    # raw_response = res.json()["response"]

    #print("[DEBUG] URL:", llm_api)
    #print(f"(LLM)[DEBUG] Model: {model}")
    print("[DEBUG] Status code:", res.status_code)
    print("[DEBUG] Response text:", res.text)
    print(f"(LLM)[DEBUG] Raw response:\n{raw_response}")

    match = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print(f"(LLM)[DEBUG] SQL Detected and cleaned:\n{cleaned_sql}")
        return cleaned_sql

    return raw_response

def generate_json_plan(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert who generates JSON plans from templates."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,  
        "max_tokens": 1024
    }

    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    res.raise_for_status()
    raw_response = res.json()["choices"][0]["message"]["content"]
    return raw_response