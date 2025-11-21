import logging
import uuid
import time
from datetime import datetime

from utils.embed import embed_text
from db.vector_db import select_relevant_tables, select_relevant_examples
from core.parse_results import parse_results
from core.query_builder import build_query

from core import llm, prompt_builder

logging.basicConfig(
    filename="logs/query_service.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def handle_user_query(user_question: str, retries: int = 2):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    logging.info("[%s] User Question: %s", request_id, user_question)

    # 1. Embed the input
    question_embedding = embed_text(user_question)
    
    # 2: Select relevant tables and examples
    relevant_tables = select_relevant_tables(question_embedding)
    #print(f"[MAIN] Relevant tables: {relevant_tables}")

    # 3: Fetch schema and column descriptions for relevant tables and put in text form for prompting
    schema_text = prompt_builder.build_schema_prompt(relevant_tables)

    # 4: Fetch most similar examples and put in text form for prompting
    relevant_examples = select_relevant_examples(question_embedding)
    examples_text = prompt_builder.build_examples_prompt(relevant_examples)

    # 5: Build full prompt
    prompt = prompt_builder.build_full_prompt(user_question, schema_text, examples_text)
    #print(f"[MAIN] Prompt generated", prompt)

    # 6: Call LLM to generate raw JSON plan
    plan_raw = llm.generate_json_plan(prompt)
    print(f"[MAIN] Plan: {type(plan_raw)}, {plan_raw}")
    
    duration = time.time() - start_time
    logging.info("[%s] Plan Generated | Duration: %.3f sec", request_id, duration)
    
    # import json
    # plan_raw = json.loads('''
       
    # ''')

    # 7: Validate plan
    # plan = validate_json.plan.validate(plan_raw)

    # 8: Turn JSON Plan to SQL
    sql_queries = build_query(plan_raw)
    print("[MAIN] Result: ", sql_queries)

    # 9: Execute SQL statements
    layers = parse_results(sql_queries)
    logging.info("[%s] Generated SQL: %s", request_id, sql_queries)


    duration = time.time() - start_time
    logging.info("[%s] Execution Status: SUCCESS | Duration: %.3f sec", request_id, duration)

    return {
            "sql": "",
            "layers": layers,
            "error": None,
    }


def handle_manual_query(user_query: str):
    try: 
        rows, colnames, er = db.execute_sql(user_query)
        geojson, table_cols, table_rows = geo.convert(rows, colnames)
        return {
                "sql": user_query.strip(),
                "geojson": geojson,
                "columns": table_cols,
                "rows": table_rows,
                "error": None,
        }
    except Exception as e:
        print(e)

