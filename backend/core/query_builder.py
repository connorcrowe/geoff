"""
Query Builder Module

Converts structured JSON plans into executable PostGIS SQL queries.
Supports SELECT, AGGREGATE, UNION, and CTE query types with comprehensive
filtering, spatial operations, and joins.

Based on specifications in:
- docs/specs/query_builder2.md
- docs/specs/json_plan.md
"""

from typing import Dict, List, Any, Optional


def build_query(plan: Dict) -> List[str]:
    """
    Main entry point: converts a JSON plan into a list of SQL query strings.
    
    Args:
        plan: JSON plan dictionary with 'layers' array
        
    Returns:
        List of SQL query strings, one per layer
        
    Example:
        plan = {"layers": [{"layer_name": "attractions", "layer_type": "primary", ...}]}
        queries = build_query(plan)
        # Returns: ["SELECT ... FROM attractions;"]
    """
    if not plan or "layers" not in plan:
        raise ValueError("Invalid plan: missing 'layers' key")
    
    sql_queries = []
    
    for layer in plan["layers"]:
        if "query" not in layer:
            raise ValueError(f"Layer missing 'query' field: {layer.get('layer_name', 'unknown')}")
        
        query_obj = layer["query"]
        query_type = query_obj.get("type", "select")
        
        # Route to appropriate query builder based on type
        if query_type == "cte":
            sql = _build_cte_query(query_obj)
        elif query_type == "union":
            sql = _build_union_query(query_obj)
        elif query_type in ("select", "aggregate"):
            sql = _build_select_query(query_obj)
        else:
            raise ValueError(f"Unknown query type: {query_type}")
        
        sql_queries.append(sql)
    
    return sql_queries


def _build_select_query(query: Dict) -> str:
    """
    Build a SELECT or AGGREGATE query from query object.
    
    Handles: SELECT, FROM, JOIN, WHERE, spatial filters, GROUP BY, ORDER BY, LIMIT
    """
    parts = []
    
    # SELECT clause
    distinct = "DISTINCT " if query.get("distinct", False) else ""
    select_clause = _build_select_clause(query)
    parts.append(f"SELECT {distinct}{select_clause}")
    
    # FROM clause
    from_clause = _build_from_clause(query)
    parts.append(f"FROM {from_clause}")
    
    # JOIN clauses
    if "joins" in query and query["joins"]:
        join_clauses = _build_joins(query)
        parts.extend(join_clauses)
    
    # WHERE clause (regular filters + spatial filters)
    where_conditions = []
    
    if "filters" in query and query["filters"]:
        filter_clause = _build_where_clause(query["filters"])
        if filter_clause:
            where_conditions.append(f"({filter_clause})")
    
    if "spatial_filters" in query and query["spatial_filters"]:
        spatial_clauses = _build_spatial_filters(query)
        where_conditions.extend(spatial_clauses)
    
    if where_conditions:
        parts.append(f"WHERE {' AND '.join(where_conditions)}")
    
    # GROUP BY clause
    if "group_by" in query and query["group_by"]:
        group_by_clause = _build_group_by(query["group_by"])
        parts.append(f"GROUP BY {group_by_clause}")
    
    # ORDER BY clause
    if "order_by" in query and query["order_by"]:
        order_by_clause = _build_order_by(query["order_by"])
        parts.append(f"ORDER BY {order_by_clause}")
    
    # LIMIT clause
    if "limit" in query and query["limit"]:
        parts.append(f"LIMIT {int(query['limit'])}")
    
    return " ".join(parts) + ";"


def _build_select_clause(query: Dict) -> str:
    """
    Build SELECT clause from columns array.
    
    Handles:
    - Simple columns: {"name": "name"}
    - Aliased columns: {"name": "ward_id", "alias": "ward_identifier"}
    - Prefixed columns: {"name": "fs.station_no"} - for disambiguation in joins
    - Computed columns: {"expression": "ST_Length(geometry::geography)", "alias": "length_m"}
    - Aggregate columns: {"aggregate": "sum", "expression": "ST_Area(...)", "alias": "total_area"}
    - Formatted columns: {"expression": "to_char(...)", "alias": "formatted_value"}
    
    Note: Column names are used exactly as specified in the JSON plan. When joins are
    present, the JSON plan must include table prefixes (e.g., "fs.address") to avoid
    ambiguous column references.
    """
    if not query.get("columns"):
        raise ValueError("Query must have 'columns' array")
    
    column_parts = []
    
    for col in query["columns"]:
        # Handle expression-based columns (computed, formatted, geometry)
        if "expression" in col:
            expr = col["expression"]
            # If aggregate function specified, wrap expression
            if "aggregate" in col:
                agg_func = col["aggregate"].upper()
                expr = f"{agg_func}({expr})"
            
            # Add alias if provided
            if "alias" in col:
                column_parts.append(f"{expr} AS {col['alias']}")
            else:
                column_parts.append(expr)
        
        # Handle simple column names - use exactly as specified
        elif "name" in col:
            col_name = col["name"]
            
            # Use column name exactly as provided (no automatic prefixing)
            # The JSON plan is responsible for including table prefixes when needed
            col_ref = col_name
            
            # Apply aggregate function if specified
            if "aggregate" in col:
                agg_func = col["aggregate"].upper()
                col_ref = f"{agg_func}({col_ref})"
            
            # Add alias if provided
            if "alias" in col:
                column_parts.append(f"{col_ref} AS {col['alias']}")
            else:
                column_parts.append(col_ref)
        
        else:
            raise ValueError(f"Column must have 'name' or 'expression': {col}")
    
    return ", ".join(column_parts)


def _build_from_clause(query: Dict) -> str:
    """
    Build FROM clause with optional table alias.
    
    Example: "attractions" or "attractions AS a"
    """
    if not query.get("table"):
        raise ValueError("Query must have 'table' field")
    
    table = query["table"]
    alias = query.get("alias")
    
    if alias:
        return f"{table} AS {alias}"
    return table


def _build_where_clause(filters: List[Dict]) -> str:
    """
    Build WHERE clause from filter objects.
    
    Supports operators: <, <=, >, >=, =, !=, ILIKE, NOT ILIKE, BETWEEN, IN, IS NULL, IS NOT NULL
    Supports logic: AND, OR
    
    Example filters:
        [{"column": "year_built", "operator": "<", "value": 1980}]
        [{"column": "lane_type", "operator": "ILIKE", "value": "%protected%"},
         {"column": "installed_year", "operator": ">=", "value": 2020, "logic": "AND"}]
    """
    if not filters:
        return ""
    
    conditions = []
    
    for i, filter_obj in enumerate(filters):
        column = filter_obj["column"]
        operator = filter_obj["operator"].upper()
        value = filter_obj.get("value")
        
        # Build condition based on operator
        if operator in ("IS NULL", "IS NOT NULL"):
            condition = f"{column} {operator}"
        
        elif operator == "BETWEEN":
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError(f"BETWEEN requires array of 2 values: {value}")
            val1 = _format_value(value[0])
            val2 = _format_value(value[1])
            condition = f"{column} BETWEEN {val1} AND {val2}"
        
        elif operator == "NOT BETWEEN":
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError(f"NOT BETWEEN requires array of 2 values: {value}")
            val1 = _format_value(value[0])
            val2 = _format_value(value[1])
            condition = f"{column} NOT BETWEEN {val1} AND {val2}"
        
        elif operator in ("IN", "NOT IN"):
            if not isinstance(value, list):
                raise ValueError(f"{operator} requires array value: {value}")
            formatted_values = ", ".join(_format_value(v) for v in value)
            condition = f"{column} {operator} ({formatted_values})"
        
        else:
            # Standard comparison operators
            formatted_value = _format_value(value)
            condition = f"{column} {operator} {formatted_value}"
        
        # Add logical operator if not first condition
        if i > 0:
            logic = filter_obj.get("logic", "AND").upper()
            conditions.append(f"{logic} {condition}")
        else:
            conditions.append(condition)
    
    return " ".join(conditions)


def _build_spatial_filters(query: Dict) -> List[str]:
    """
    Build spatial filter clauses using EXISTS subqueries.
    
    Example:
        {
            "operation": "ST_DWithin",
            "target_table": "schools",
            "distance": 500,
            "use_exists": true
        }
    
    Returns:
        ["EXISTS (SELECT 1 FROM schools WHERE ST_DWithin(...))"]
    """
    spatial_filters = query.get("spatial_filters", [])
    table = query.get("table")
    table_alias = query.get("alias", table)
    
    clauses = []
    
    for sf in spatial_filters:
        operation = sf["operation"]
        target_table = sf["target_table"]
        use_exists = sf.get("use_exists", True)
        
        # Build spatial condition
        if operation == "ST_DWithin":
            distance = sf.get("distance")
            if distance is None:
                raise ValueError("ST_DWithin requires 'distance' parameter")
            spatial_condition = (
                f"ST_DWithin({table_alias}.geometry::geography, "
                f"{target_table}.geometry::geography, {distance})"
            )
        elif operation in ("ST_Intersects", "ST_Contains", "ST_Within"):
            spatial_condition = f"{operation}({table_alias}.geometry, {target_table}.geometry)"
        else:
            raise ValueError(f"Unknown spatial operation: {operation}")
        
        # Wrap in EXISTS subquery if requested
        if use_exists:
            clause = f"EXISTS (SELECT 1 FROM {target_table} WHERE {spatial_condition})"
        else:
            clause = spatial_condition
        
        clauses.append(clause)
    
    return clauses


def _build_joins(query: Dict) -> List[str]:
    """
    Build JOIN clauses from join objects.
    
    Supports:
    - Spatial joins: ST_DWithin, ST_Intersects, ST_Contains, ST_Within
    - Attribute joins: equality on specified columns
    
    Example:
        {
            "type": "INNER",
            "table": "fire_stations",
            "alias": "fs",
            "condition": {
                "type": "spatial",
                "operation": "ST_DWithin",
                "distance": 1000
            }
        }
    """
    joins = query.get("joins", [])
    base_table_alias = query.get("alias", query.get("table"))
    
    join_clauses = []
    
    for join in joins:
        join_type = join.get("type", "INNER").upper()
        join_table = join["table"]
        join_alias = join.get("alias", join_table)
        condition = join["condition"]
        
        # Build join condition based on type
        if condition["type"] == "spatial":
            operation = condition["operation"]
            
            if operation == "ST_DWithin":
                distance = condition.get("distance")
                if distance is None:
                    raise ValueError("ST_DWithin join requires 'distance'")
                join_condition = (
                    f"ST_DWithin({base_table_alias}.geometry::geography, "
                    f"{join_alias}.geometry::geography, {distance})"
                )
            elif operation in ("ST_Intersects", "ST_Contains", "ST_Within"):
                join_condition = (
                    f"{operation}({base_table_alias}.geometry, {join_alias}.geometry)"
                )
            else:
                raise ValueError(f"Unknown spatial join operation: {operation}")
        
        elif condition["type"] == "attribute":
            left_col = condition["left_column"]
            right_col = condition["right_column"]
            
            # Add table prefixes if not present
            if "." not in left_col:
                left_col = f"{base_table_alias}.{left_col}"
            if "." not in right_col:
                right_col = f"{join_alias}.{right_col}"
            
            join_condition = f"{left_col} = {right_col}"
        
        else:
            raise ValueError(f"Unknown join condition type: {condition['type']}")
        
        # Build full JOIN clause
        if join_alias != join_table:
            join_clause = f"{join_type} JOIN {join_table} AS {join_alias} ON {join_condition}"
        else:
            join_clause = f"{join_type} JOIN {join_table} ON {join_condition}"
        
        join_clauses.append(join_clause)
    
    return join_clauses


def _build_group_by(group_by: List[str]) -> str:
    """
    Build GROUP BY clause from list of column names.
    
    Example: ["n.id", "n.area_name", "n.geometry"]
    Returns: "n.id, n.area_name, n.geometry"
    """
    if not group_by:
        return ""
    
    return ", ".join(group_by)


def _build_order_by(order_by: List[Dict]) -> str:
    """
    Build ORDER BY clause from order objects.
    
    Example:
        [{"column": "name", "direction": "ASC"}]
        [{"expression": "ST_Length(geometry::geography)", "direction": "DESC"}]
    """
    if not order_by:
        return ""
    
    order_parts = []
    
    for order in order_by:
        direction = order.get("direction", "ASC").upper()
        
        if "expression" in order:
            order_parts.append(f"{order['expression']} {direction}")
        elif "column" in order:
            order_parts.append(f"{order['column']} {direction}")
        else:
            raise ValueError(f"Order must have 'column' or 'expression': {order}")
    
    return ", ".join(order_parts)


def _build_union_query(query: Dict) -> str:
    """
    Build UNION query from multiple sub-queries.
    
    Example:
        {
            "type": "union",
            "union_type": "ALL",
            "queries": [query1, query2, query3]
        }
    """
    if "queries" not in query or not query["queries"]:
        raise ValueError("UNION query must have 'queries' array")
    
    union_type = query.get("union_type", "ALL").upper()
    if union_type not in ("ALL", "DISTINCT", ""):
        raise ValueError(f"Invalid union_type: {union_type}")
    
    # Build each sub-query (remove trailing semicolon)
    sub_queries = []
    for sub_query in query["queries"]:
        sql = _build_select_query(sub_query)
        # Remove semicolon if present
        sql = sql.rstrip(";")
        sub_queries.append(sql)
    
    # Join with UNION or UNION ALL
    union_operator = f"UNION {union_type}" if union_type else "UNION"
    return f" {union_operator} ".join(sub_queries) + ";"


def _build_cte_query(query: Dict) -> str:
    """
    Build CTE (Common Table Expression) query.
    
    Example:
        {
            "type": "cte",
            "ctes": [
                {
                    "name": "park_counts",
                    "query": {...}
                }
            ],
            "main_query": {...}
        }
    """
    if "ctes" not in query or not query["ctes"]:
        raise ValueError("CTE query must have 'ctes' array")
    if "main_query" not in query:
        raise ValueError("CTE query must have 'main_query'")
    
    cte_parts = []
    
    # Build each CTE
    for cte in query["ctes"]:
        cte_name = cte["name"]
        cte_query = cte["query"]
        
        # Build the CTE query (remove trailing semicolon)
        cte_sql = _build_select_query(cte_query).rstrip(";")
        cte_parts.append(f"{cte_name} AS ({cte_sql})")
    
    # Build main query (remove trailing semicolon)
    main_sql = _build_select_query(query["main_query"]).rstrip(";")
    
    # Combine: WITH cte1 AS (...), cte2 AS (...) main_query
    ctes_clause = ", ".join(cte_parts)
    return f"WITH {ctes_clause} {main_sql};"


def _format_value(value: Any) -> str:
    """
    Format a value for SQL insertion.
    
    Handles:
    - None -> NULL
    - Strings -> 'escaped string'
    - Numbers -> number
    - Booleans -> TRUE/FALSE
    """
    if value is None:
        return "NULL"
    
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    
    if isinstance(value, (int, float)):
        return str(value)
    
    if isinstance(value, str):
        # Escape single quotes by doubling them
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    
    # Fallback: convert to string and quote
    return f"'{str(value)}'"