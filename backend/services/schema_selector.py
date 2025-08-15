# services/schema_selector.py
""""""

from config.schemas import schemas
from config.schema_keywords import schema_keywords

def select_schemas_from_query(query: str, min_results: int=1):
    """
    Search user query for keywords associated with specific database tables.
    Returns a list of matching table names.
    Falls back to all schemas if none found.
    """
    query_lower = query.lower()
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