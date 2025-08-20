from config.examples import examples
from config.schemas import schemas
from config.schema_keywords import schema_keywords
from config.prompts import SYSTEM_PROMPT, CORRECTIVE_PROMPT

def select_tables(user_question: str, min_results: int=1):
    """
    Search user query for keywords associated with specific database tables.
    Returns a list of matching table names.
    Falls back to all schemas if none found.
    """
    query_lower = user_question.lower()
    matched_tables = [
        table for table, keywords in schema_keywords.items()
        if any(keyword in query_lower for keyword in keywords)
    ]

    if len(matched_tables) < min_results:
        matched_tables = list(schemas.keys())

    return matched_tables

# def select_examples_from_tables(tables, user_query, n=4):
#     """Return up to n relevant examples for the given tables."""
#     # TODO: Add sequence matching and rank examples to select best ones
#     return None

def build_schema_prompt(table_list):
    """Return only relevant schemas as a string for LLM system prompt."""
    return "\n".join(schemas[table] for table in table_list if table in schemas)

def build_examples_prompt(tables, n=5):
    """Format example list into Q/A style for LLM system prompt."""
    formatted = []

    example_list = [ex for ex in examples if set(ex['tables']).issubset(set(tables))][:n]

    for ex in example_list:
        formatted.append(f"Q: {ex['user_query']}\nA: {ex['sql'].strip()}")
    return "\n".join(formatted)

def build_full_prompt(user_question: str, schema_prompt, examples_prompt, previous_sql: str=None, previous_error: str=None):

    if previous_sql and previous_error:
        # Corrective prompt
        prompt_text = CORRECTIVE_PROMPT.render(
            schema_prompt=schema_prompt,
            previous_sql=previous_sql,
            error_message=previous_error,
            user_question=user_question
        )
    else:
        # Normal (first) query
        prompt_text = SYSTEM_PROMPT.render(
            schema_prompt=schema_prompt,
            few_shot_examples=examples_prompt,
            user_question=user_question
        )
    return prompt_text