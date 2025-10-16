import logging
import uuid
import time
from datetime import datetime
import json

from core import geo, llm, prompt_builder
from utils import embed
from db.vector_db import select_relevant_tables
from db.db import execute_sql
from core.query_builder import build_query

logging.basicConfig(
    filename="logs/query_service.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def handle_user_query(user_question: str, retries: int = 2):
    start_time = time.time()

    # 1. Embed the input
    question_embedding = embed.embed_text(user_question)
    
    # 1: Select relevant tables and examples
    relevant_tables = select_relevant_tables(question_embedding)
    #print(f"[MAIN] Relevant tables: {relevant_tables}")

    # 2: Fetch schema and column descriptions for relevant tables
    schema_text = prompt_builder.build_schema_prompt(relevant_tables)

    # 3: Fetch most similar examples
    examples_text = prompt_builder.build_examples_prompt(relevant_tables)

    # 4: Build full prompt
    prompt = prompt_builder.build_full_prompt(user_question, schema_text, examples_text)
    print(f"[MAIN] Prompt: {prompt}")

    # 5: Call LLM to generate raw JSON plan
    plan_raw = llm.generate_json_plan(prompt)
    print(f"[MAIN] Plan: {type(plan_raw)}, {plan_raw}")

    plan_raw = plan_raw.lstrip("`").lstrip("json").rstrip("`").strip()
    print("AAA", plan_raw)
    # 6: Validate plan
    # plan = validate_json.plan.validate(plan_raw)

    # 7: Execute plan
    plan_dict = json.loads(plan_raw)
    result = build_query(plan_dict)
    print("RESULT: ", result[0])
    rows, colnames, er = execute_sql(result[0])
    layers = geo.convert_to_geo_layers(rows, colnames)
    print(layers)

    return {
            "sql": "",
            "layers": layers,
            "error": None,
    }


    # TODO: Fix logging
    #request_id = str(uuid.uuid4())
    #logging.info("[%s] User Question: %s", request_id, user_question)
    #logging.info("[%s] Generated SQL: %s", request_id, sql)

    # # 4: Execute
    # try:
    #     rows, colnames, er = db.execute_sql(sql)
    #     layers = geo.convert_to_geo_layers(rows, colnames)

    #     duration = time.time() - start_time
    #     logging.info("[%s] Execution Status: SUCCESS | Duration: %.3f sec", request_id, duration)

    #     return {
    #         "sql": sql.strip(),
    #         "layers": layers,
    #         "error": None,
    #     }

    # except Exception as e:
    #     duration = time.time() - start_time
    #     logging.error("[%s] Execution Status: FAILURE | Duration: %.3f sec | Error: %s", request_id, duration, str(e))

# def handle_user_query(user_question: str, retries: int = 2):
#     start_time = time.time()
    
#     # 1: Select relevant tables and examples
#     relevant_tables = prompt_builder.select_tables(user_question)

#     print(f"[MAIN] Relevant tables: {relevant_tables}")

#     schema_prompt = prompt_builder.build_schema_prompt(relevant_tables)
#     examples_prompt = prompt_builder.build_examples_prompt(relevant_tables)

#     previous_sql = None
#     previous_error = None
#     for attempt in range(retries + 1):
        
#         # 2: Build prompt for LLM
#         llm_prompt = prompt_builder.build_full_prompt(user_question, schema_prompt, examples_prompt, previous_sql, previous_error)

#         # 3: Generate SQL
#         sql = llm.generate_sql(llm_prompt)

#         request_id = str(uuid.uuid4())
#         logging.info("[%s] User Question: %s", request_id, user_question)
#         logging.info("[%s] Generated SQL: %s", request_id, sql)

#         # 4: Execute
#         try:
#             rows, colnames, er = db.execute_sql(sql)
#             layers = geo.convert_to_geo_layers(rows, colnames)

#             duration = time.time() - start_time
#             logging.info("[%s] Execution Status: SUCCESS | Duration: %.3f sec", request_id, duration)

#             return {
#                 "sql": sql.strip(),
#                 "layers": layers,
#                 "error": None,
#             }

#         except Exception as e:
#             duration = time.time() - start_time
#             logging.error("[%s] Execution Status: FAILURE | Duration: %.3f sec | Error: %s", request_id, duration, str(e))

#             if attempt >= retries:
#                 return {"sql": sql, "error": str(e)}
#             previous_sql = sql
#             previous_error = e

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

