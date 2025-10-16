from typing import Dict, List

def build_query(plan: Dict) -> List[str]:

    action = plan.get("action")
    if not action:
        raise ValueError("Plan missing 'action' field")
    
    match action:
        case "select":
            return _build_select(plan)
        case _:
            raise NotImplementedError(f"Action ({action}) not supported")

def _build_select(plan: Dict) -> List[str]:
    sql_queries = []
    for source in plan.get("source_tables", []):
        table = source["table"]
        columns = source.get("columns", ["*"])
        filters = source.get("filters", [])

        where_clause = ""
        if filters:
            clauses = []
            for f in filters:
                col, op, value = f["column"], f["operator"], f["value"]
                if isinstance(value, str): value = f"'{value}'"
                clauses.append(f"{col} {op} {value}")
            where_clause = " WHERE " + " AND ".join(clauses)

        query = f"SELECT {', '.join(columns)} FROM {table}{where_clause};"
        sql_queries.append(query.strip())
    
    return sql_queries