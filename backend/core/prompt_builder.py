def build_schema_prompt(relevant_tables):
    """Return only relevant schemas as a string for LLM system prompt."""
    schema_parts = []
    for table in relevant_tables:
        columns_text = "\n".join(
            f"  - {c['column_name']} ({c['col_type']}): {c['description']}"
            for c in table["columns"]
        )
        schema_parts.append(f"Table: {table['table_name']}\n{columns_text}")
    schema_text = "\n\n".join(schema_parts)
    return schema_text

def build_examples_prompt(relevant_examples, n=10):
    """Format example list into Q/A style for LLM system prompt."""
    example_parts = []
    for ex in relevant_examples:
        example_parts.append(
            f"User Query: {ex['user_query']}\nPlan:\n{ex['plan']}"
        )
    examples_text = "\n\n".join(example_parts)
    
    return examples_text

def build_full_prompt(user_question: str, schema_text, examples_text, previous_sql: str=None, previous_error: str=None):
    prompt_text = f"""
*User Question*:
    {user_question}

*Database Schema*:
{schema_text}

*Example Queries and Resulting JSON Plans*:
{examples_text}

*Instructions*:
    Using the schema above and examples, generate a JSON plan that answers the user question.
    Include tables, columns, filters, joins, and output fields.
    Only include relevant tables and columns.
    """
    return prompt_text