import logging
import uuid
import time
from datetime import datetime

from core import db, geo, llm, prompt_builder

logging.basicConfig(
    filename="logs/query_service.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def handle_user_query(user_question: str, retries: int = 2):
    start_time = time.time()
    
    # 1: Select relevant tables and examples
    relevant_tables = prompt_builder.select_tables(user_question)

    print(f"[MAIN] Relevant tables: {relevant_tables}")

    schema_prompt = prompt_builder.build_schema_prompt(relevant_tables)
    examples_prompt = prompt_builder.build_examples_prompt(relevant_tables)

    previous_sql = None
    previous_error = None
    for attempt in range(retries + 1):
        
        # 2: Build prompt for LLM
        llm_prompt = prompt_builder.build_full_prompt(user_question, schema_prompt, examples_prompt, previous_sql, previous_error)
        #print(f"[MAIN] System Prompt: {llm_prompt}")

        # 3: Generate SQL
        sql = llm.generate_sql(llm_prompt)

        # Log prompt and resulting SQL
        request_id = str(uuid.uuid4())
        logging.info("[%s] User Question: %s", request_id, user_question)
        logging.info("[%s] Generated SQL: %s", request_id, sql)

        # 4: Execute
        try:
            # TODO: Double try perhaps not needed here
            rows, colnames, er = db.execute_sql(sql)
            geojson, table_cols, table_rows = geo.convert(rows, colnames)

            duration = time.time() - start_time
            logging.info("[%s] Execution Status: SUCCESS | Duration: %.3f sec", request_id, duration)

            return {
                "sql": sql.strip(),
                "geojson": geojson,
                "columns": table_cols,
                "rows": table_rows,
                "error": None,
            }

        except Exception as e:
            duration = time.time() - start_time
            logging.error("[%s] Execution Status: FAILURE | Duration: %.3f sec | Error: %s", request_id, duration, str(e))

            if attempt >= retries:
                return {"sql": sql, "error": str(e)}
            previous_sql = sql
            previous_error = e

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

