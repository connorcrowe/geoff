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

# --------------------------
# SELECT BUILDER
# --------------------------

def _build_select(plan: Dict) -> List[str]:
    """
    Builds SQL SELECT statements for each group.
    Handles spatial or attribute relations, filtering, and joining.
    """
    print("[QB] Building SELECT queries")
    sql_queries = []

    for group_idx, group in enumerate(plan.get("groups", [])):
        print(f"[QB] Processing group {group_idx + 1}")

        # --- Build subqueries for all tables ---
        subqueries, aliases = {}, {}
        source_tables = group.get("source_tables", [])
        for i, table_info in enumerate(source_tables):
            alias = f"t{i+1}"
            aliases[table_info["table"]] = alias
            subqueries[table_info["table"]] = __build_subquery(table_info, alias)
            print(f"[QB] Built subquery for {table_info['table']}, query: {subqueries[table_info['table']]}")

        relations = group.get("relations", [])

        # --- If no relations, return each table independently ---
        if not relations:
            for tbl, sub in subqueries.items():
                sql_queries.append(__finalize_query(sub, geom_col="geometry"))
            continue

        # --- Process relations (currently one per group) ---
        relation = relations[0]
        clause = relation.get("clause", "join").lower()
        relation_type = relation.get("type", "spatial").lower()

        if relation_type == "spatial":
            spatial_queries = __build_spatial_relation(
                relation, subqueries, aliases
            )
            # Finalize all spatial queries to GeoJSON
            sql_queries.extend([__finalize_query(q, geom_col="geometry") for q in spatial_queries])

        elif relation_type == "attribute":
            attr_query = __build_attribute_relation(
                relation, subqueries, aliases
            )
            sql_queries.append(__finalize_query(attr_query, geom_col="geometry"))

        else:
            raise NotImplementedError(f"Relation type '{relation_type}' not supported")

    return sql_queries

# ---------------------------------------------------------------------
# SUBQUERY BUILDER
# ---------------------------------------------------------------------

def __build_subquery(table_info: Dict, alias: str) -> str:
    columns = table_info.get("columns", ["*"])
    filters = table_info.get("filters", [])

    processed_columns = columns
    
    # Handle table level filter
    where_clause = ""
    if filters:
        clauses = []
        for f in filters:
            col, op, value = f["column"], f["operator"], f["value"]
            if isinstance(value, str): value = f"'{value}'"
            clauses.append(f"{col} {op} {value}")
        where_clause = " WHERE " + " AND ".join(clauses)

    subquery = f"SELECT {', '.join(processed_columns)} FROM {table_info['table']} AS {alias}" + where_clause
    return subquery

# ---------------------------------------------------------------------
# SPATIAL RELATIONS
# ---------------------------------------------------------------------

def __build_spatial_relation(rel: Dict, subqueries: Dict[str, str], aliases: Dict[str, str]) -> List[str]:
    """Handles spatial joins and filters between two tables."""
    left = rel["left_table"]
    right = rel["right_table"]
    left_alias = aliases[left]
    right_alias = aliases[right]

    method = rel.get("method", "st_intersects").lower()
    clause = rel.get("clause", "join").lower()
    params = rel.get("params", {})

    # Build condition with ::geography casting
    if method == "st_dwithin":
        dist = params.get("distance_meters", 0)
        condition = f"ST_DWithin({left_alias}.geometry::geography, {right_alias}.geometry::geography, {dist})"
    elif method == "st_intersects":
        # For intersects, geography cast is not needed; use geometry
        condition = f"ST_Intersects({left_alias}.geometry, {right_alias}.geometry)"
    else:
        raise NotImplementedError(f"Spatial method '{method}' not supported")

    left_cols = __get_processed_columns(subqueries[left], left_alias)
    right_cols = __get_processed_columns(subqueries[right], right_alias)

    queries = []

    # --- CASE 1: EXISTS / spatial filter ---
    if clause == "exists":
        # Query 1: filtered left
        q1 = (
            f"SELECT DISTINCT {', '.join(left_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"WHERE EXISTS (SELECT 1 FROM ({subqueries[right]}) AS {right_alias} "
            f"WHERE {condition})"
        )

        # Query 2: the right layer (for context)
        q2 = f"{subqueries[right]}"

        queries.extend([q1, q2])

    # --- CASE 2: JOIN ---
    elif clause == "join":
        q = (
            f"SELECT {', '.join(left_cols + right_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"JOIN ({subqueries[right]}) AS {right_alias} "
            f"ON {condition}"
        )
        queries.append(q)

    # --- CASE 3: LEFT JOIN ---
    elif clause == "left_join":
        q = (
            f"SELECT {', '.join(left_cols + right_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"LEFT JOIN ({subqueries[right]}) AS {right_alias} "
            f"ON {condition}"
        )
        queries.append(q)

    else:
        raise NotImplementedError(f"Spatial clause '{clause}' not supported")

    return queries


# ---------------------------------------------------------------------
# ATTRIBUTE RELATIONS
# ---------------------------------------------------------------------

def __build_attribute_relation(rel: Dict, subqueries: Dict[str, str], aliases: Dict[str, str]) -> str:
    """Handles non-spatial (attribute) joins."""
    left = rel["left_table"]
    right = rel["right_table"]
    left_alias = aliases[left]
    right_alias = aliases[right]

    on = rel.get("on", {})
    left_col, right_col = on.get("left_column"), on.get("right_column")
    clause = rel.get("clause", "join").lower()

    condition = f"{left_alias}.{left_col} = {right_alias}.{right_col}"

    left_cols = __get_processed_columns(subqueries[left], left_alias)
    right_cols = __get_processed_columns(subqueries[right], right_alias)

    if clause == "join":
        return (
            f"SELECT {', '.join(left_cols + right_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"JOIN ({subqueries[right]}) AS {right_alias} "
            f"ON {condition}"
        )

    elif clause == "left_join":
        return (
            f"SELECT {', '.join(left_cols + right_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"LEFT JOIN ({subqueries[right]}) AS {right_alias} "
            f"ON {condition}"
        )

    elif clause == "exists":
        return (
            f"SELECT DISTINCT {', '.join(left_cols)} "
            f"FROM ({subqueries[left]}) AS {left_alias} "
            f"WHERE EXISTS (SELECT 1 FROM ({subqueries[right]}) AS {right_alias} "
            f"WHERE {condition})"
        )

    else:
        raise NotImplementedError(f"Attribute clause '{clause}' not supported")


# ---------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------

def __get_processed_columns(subquery: str, alias: str) -> List[str]:
    """
    Extract column list for select statement reuse.
    Currently assumes subquery already includes selected columns.
    """
    # Since can't easily parse SQL, just return alias.* for now.
    # This can later be improved with regex or explicit column tracking.
    return [f"{alias}.*"]

def __finalize_query(raw_query: str, geom_col: str = "geometry") -> str:
    return (
        f"SELECT *, ST_AsGeoJSON({geom_col}) AS {geom_col} "
        f"FROM ({raw_query}) AS sub;"
    )