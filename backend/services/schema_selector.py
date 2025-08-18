# services/schema_selector.py
""""""

from config.schemas import schemas
from config.schema_keywords import schema_keywords
from config.examples import examples

def select_schemas_from_query(user_query: str, min_results: int=1):
    """
    Search user query for keywords associated with specific database tables.
    Returns a list of matching table names.
    Falls back to all schemas if none found.
    """
    query_lower = user_query.lower()
    matched_tables = [
        table for table, keywords in schema_keywords.items()
        if any(keyword in query_lower for keyword in keywords)
    ]

    if len(matched_tables) < min_results:
        matched_tables = list(schemas.keys())

    return matched_tables

def build_schema_prompt(table_list):
    """Return only relevant schemas as a string for LLM system prompt."""
    return "\n".join(schemas[table] for table in table_list if table in schemas)

def select_examples_from_tables(tables, user_query, n=4):
    """Return up to n relevant examples for the given tables."""
    # TODO: Add sequence matching and rank examples to select best ones

    example_list = [ex for ex in examples if set(ex['tables']).issubset(set(tables))]
    return example_list[:n]

def build_example_prompt(examples_list):
    """Format example list into Q/A style for LLM system prompt."""
    formatted = []
    for ex in examples_list:
        formatted.append(f"Q: {ex['user_query']}\nA: {ex['sql'].strip()}")
    return "\n".join(formatted)