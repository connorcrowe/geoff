import requests
import re

from dotenv import load_dotenv
from pathlib import Path
import os

from services.schema_selector import select_schemas_from_query, build_schema_prompt, select_examples_from_tables, build_example_prompt
from config.prompts import SYSTEM_PROMPT, CORRECTIVE_PROMPT

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

llm_api = os.getenv("LLM_API_URL")

def generate_sql_from_prompt(user_prompt: str, previous_sql: str=None, error_message: str=None) -> str:
    relevant_tables = select_schemas_from_query(user_prompt)
    schema_prompt = build_schema_prompt(relevant_tables)
    
    example_list = select_examples_from_tables(relevant_tables, user_prompt, 4)
    few_shot_examples = build_example_prompt(example_list)
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
            few_shot_examples=few_shot_examples,
            user_question=user_prompt
        )
    print(f"(LLM)[DEBUG] Prompt Text:\n{prompt_text}")

    model = "llama3.2"
    res = requests.post(
        llm_api,
        json={
            "model": model,
            "prompt": prompt_text,
            "stream": False
        }
    )
    print(f"(LLM)[DEBUG] Model: {model}")
    raw_response = res.json()["response"]

    print(f"(LLM)[DEBUG] Raw response:\n{res.json()["response"]}")
    match = re.search(r"(SELECT[\s\S]+?;)", raw_response, re.IGNORECASE)
    if match:
        cleaned_sql = match.group(1).strip()
        print(f"(LLM)[DEBUG] SQL Detected and cleaned:\n{cleaned_sql}")
        return cleaned_sql

    return res.json()["response"]

def test_prompt_to_sql(prompt: str) -> str:
    return "SELECT geometry FROM bike_lanes;"