import requests
import re

from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

llm_api = os.getenv("LLM_API_URL")

def prompt_to_sql(prompt: str) -> str:
    system_prompt = open("system_prompt.md").read()
    full_prompt = f"System prompt: {system_prompt}\n\nUser question: {prompt}"

    res = requests.post(
        llm_api,
        json={
            "model": "sqlcoder",
            "prompt": full_prompt,
            "stream": False
        }
    )
    #print("Raw response:", res.text)  # Debug line to see what's coming back
    print("Raw response:", res.json()["response"])

    raw_response = res.json()["response"]
    match  = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print("SQL:", cleaned_sql)
        print("END SQL")
        return cleaned_sql

    # Now try json parse
    return res.json()["response"]

def test_prompt_to_sql(prompt: str) -> str:
    return "SELECT geometry FROM bike_lanes;"