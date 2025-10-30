import re

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

    # Group level
    for group_idx, group in enumerate(plan.get("groups", [])):

        source_tables = group.get("source_tables", [])
        relations = group.get("relations", [])

        # Relation: None
        if not relations:
            for table in source_tables:
                cols = _format_columns(table.get("columns", ["*"]), table=table['table'])
                filters = _build_filters(table.get("filters", []))
                sql = f"SELECT {cols} FROM {table['table']} {filters}".strip()
                sql_queries.append(_package_query(sql))
                print(sql_queries)
            continue

        relation = relations[0]
        clause = relation.get("clause").lower()
        relation_type = relation.get("type").lower()
        method = relation.get("method", "").lower()

        left_table = relation.get("left_table")
        right_table = relation.get("right_table")
        params = relation.get("params", {})

        left_info = next((t for t in source_tables if t["table"] == left_table), None)
        right_info = next((t for t in source_tables if t["table"] == right_table), None)
        if not left_info or not right_info:
            continue

        distance = params.get("distance_meters", 0)
        spatial_func = method.upper()  # e.g., ST_DWITHIN or ST_INTERSECTS

        if spatial_func.upper() == "ST_DWITHIN":
            # ST_DWithin requires distance
            spatial_expr = f"{spatial_func}({left_table}.geometry::geography, {right_table}.geometry::geography, {distance})"
        else:
            # ST_Intersects or other 2-arg functions
            spatial_expr = f"{spatial_func}({left_table}.geometry::geography, {right_table}.geometry::geography)"

        left_key = params.get("left_column")
        right_key = params.get("right_column")
        attibute_expr = f"({left_table}.{left_key} {method} {right_table}.{right_key})"

        # Relation: Exists
        # --- EXISTS ---
        if clause == "exists" and relation_type == "spatial":
            left_cols = _format_columns(left_info.get("columns", ["*"]), table=left_table)
            right_cols = _format_columns(right_info.get("columns", ["geometry"]), table=right_table)

            left_filters = _build_filters(left_info.get("filters", []))
            right_filters = _build_filters(right_info.get("filters", []))

            expr_and_right = (f"{right_filters} AND {spatial_expr}") if right_filters else f"WHERE {spatial_expr}"

            # Left query filtered by spatial exists
            left_sql = f"""
            SELECT DISTINCT {left_cols}
            FROM {left_table}
            WHERE EXISTS (
                SELECT 1 FROM {right_table}
                {expr_and_right}
            )
            """.strip()
            if left_filters:
                left_sql = left_sql.replace("WHERE", left_filters + " AND", 1)

            # Right query with geometry only
            right_sql = f"SELECT DISTINCT {right_cols} FROM {right_table} {right_filters}".strip()

            sql_queries.extend([left_sql, right_sql])

        # --- JOIN ---
        elif clause == "join" and relation_type == "spatial":
            left_cols = _format_columns(left_info.get("columns", ["*"]), table=left_table)
            right_cols = _format_columns(right_info.get("columns", ["*"]), table=right_table, exclude_geom=True)

            left_filters = _build_filters(left_info.get("filters", []))
            right_filters = _build_filters(right_info.get("filters", []))

            join_sql = f"""
            SELECT DISTINCT {left_cols}, {right_cols}
            FROM {left_table}
            JOIN {right_table}
            ON {spatial_expr}
            """.strip()

            # Merge table filters into WHERE clause if any
            combined_filters = []
            if left_filters:
                combined_filters.append(left_filters[6:])  # strip 'WHERE '
            if right_filters:
                combined_filters.append(right_filters[6:])
            if combined_filters:
                join_sql += " WHERE " + " AND ".join(combined_filters)

            sql_queries.append(join_sql)

        elif clause == "exists" and relation_type == "attribute":
            left_cols = _format_columns(left_info.get("columns", ["*"]), table=left_table)
            right_cols = _format_columns(right_info.get("columns", ["geometry"]), table=right_table)

            left_filters = _build_filters(left_info.get("filters", []))
            right_filters = _build_filters(right_info.get("filters", []))

            expr_and_right = (f"{right_filters} AND {attibute_expr}") if right_filters else f"WHERE {attibute_expr}"

            # Left query filtered by attribute exists
            left_sql = f"""
            SELECT DISTINCT {left_cols}
            FROM {left_table}
            WHERE EXISTS (
                SELECT 1 FROM {right_table}
                {expr_and_right}
            )
            """.strip()
            if left_filters:
                left_sql = left_sql.replace("WHERE", left_filters + " AND", 1)

            # Right query with geometry only
            right_sql = f"SELECT DISTINCT {right_cols} FROM {right_table} {right_filters}".strip()

            sql_queries.extend([left_sql, right_sql])

        elif clause == "join" and relation_type == "attribute":
            left_cols = _format_columns(left_info.get("columns", ["*"]), table=left_table)
            right_cols = _format_columns(right_info.get("columns", ["*"]), table=right_table, exclude_geom=True)

            left_filters = _build_filters(left_info.get("filters", []))
            right_filters = _build_filters(right_info.get("filters", []))

            join_sql = f"""
            SELECT DISTINCT {left_cols}, {right_cols}
            FROM {left_table}
            JOIN {right_table}
            ON {attibute_expr}
            """.strip()

            # Merge table filters into WHERE clause if any
            combined_filters = []
            if left_filters:
                combined_filters.append(left_filters[6:])  # strip 'WHERE '
            if right_filters:
                combined_filters.append(right_filters[6:])
            if combined_filters:
                join_sql += " WHERE " + " AND ".join(combined_filters)

            sql_queries.append(join_sql)

    return sql_queries
        
def _build_filters(filters: list) -> str:
    if not filters: return ""

    clauses = []
    for f in filters: 
        col, op, val = f.get("column"), f.get("operator"), f.get("value")
        # Handle strings safely
        if isinstance(val, str):
            val = f"'{val}'"
        clauses.append(f"{col} {op} {val}")
    return "WHERE " + " AND ".join(clauses)

def _format_columns(columns: list[str], table: str=None, exclude_geom: bool=False) -> str:
    formatted = []
    for col in columns:
        # Handle geometry, turn to GeoJSON
        if col.lower() == "geometry":
            if exclude_geom: continue
            formatted.append(f"ST_AsGeoJSON({table}.{col}) AS geometry")

        # Handle single column spatial functions (ST_Area, ST_Length)    
        elif "st_" in col.lower():
            match = re.search(r'\b(ST_[A-Za-z0-9_]+)\s*\(\s*([A-Za-z0-9_."]+)\s*\)', col, re.IGNORECASE)
            
            spatial_func = match.group(1).lower()
            spatial_arg = match.group(2)
            unit = "m2" if spatial_func.lower() == "st_area" else "m"
            
            formatted.append(f"to_char( {spatial_func}({spatial_arg}::geography) "
                             f", 'FM999,999,999,999,999.99') "
                             f"as {table}_{spatial_func[3:]}_{unit}")

        # All other column types                             
        else: formatted.append(f"{table}.{col}")
    return ", ".join(formatted)

def _package_query(raw_query: str) -> str:
    return (
        f"{raw_query};"
    )