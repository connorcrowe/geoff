import requests
import re

from dotenv import load_dotenv
from pathlib import Path
import os

from services.schema_selector import select_schemas_from_query, build_schema_prompt
from config.prompts import SYSTEM_PROMPT, CORRECTIVE_PROMPT

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

llm_api = os.getenv("LLM_API_URL")

def generate_sql_from_prompt(user_prompt: str, previous_sql: str=None, error_message: str=None) -> str:
    relevant_tables = select_schemas_from_query(user_prompt)
    schema_prompt = build_schema_prompt(relevant_tables)
    print(f"(LLM)[DEBUG] Relevant Tables: {relevant_tables}")

    
    if previous_sql and error_message:
        # Corrective prompt
        prompt_text = CORRECTIVE_PROMPT.render(
            schema_prompt=schema_prompt,
            previous_sql=previous_sql,
            error_message=error_message,
            user_question=user_prompt
        )
    else:
        # Normal (first) query
        prompt_text = SYSTEM_PROMPT.render(
            schema_prompt=schema_prompt,
            user_question=user_prompt
        )
    print(f"(LLM)[DEBUG] Prompt Text:\n{prompt_text}")

    res = requests.post(
        llm_api,
        json={
            "model": "sqlcoder",
            "prompt": prompt_text,
            "stream": False
        }
    )
    raw_response = res.json()["response"]

    print(f"(LLM)[DEBUG] Raw response:\n{res.json()["response"]}")
    match = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print(f"(LLM)[DEBUG] SQL Detected and cleaned:\n{cleaned_sql}")
        return cleaned_sql

    return res.json()["response"]


def prompt_to_sql_old(prompt: str) -> str:

    # Select relevant schemas
    relevant_tables = select_schemas_from_query(prompt)

    # Build schema part of system prompt
    schema_prompt = build_schema_prompt(relevant_tables)

    # Build final system prompt for LLM
    system_prompt = (
        "You are a PostGIS expert. The following database tables are available:\n"
        f"{schema_prompt}\n\n"
        "Write a valid SQL query in PostGIS syntax to answer the user's question."
    )

    #print(f"System Prompt: {system_prompt}")
    #system_prompt = open("system_prompt.md").read()
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
    print("(LLM)[DEBUG] Raw response:", res.json()["response"])

    raw_response = res.json()["response"]
    match  = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print("(LLM)[DEBUG] SQL:", cleaned_sql)
        print("END SQL")
        return cleaned_sql

    # Now try json parse
    return res.json()["response"]

def test_prompt_to_sql(prompt: str) -> str:
    return "SELECT geometry FROM bike_lanes;"