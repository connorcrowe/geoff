# JSON Plan Structure

## Overview
This document defines the JSON plan structure that the LLM generates and the query_builder consumes to produce SQL statements.

## Top-Level Structure

```json
{
  "layers": [
    {
      "layer_name": "string",
      "layer_type": "primary|context|reference",
      "query": { /* Query Object */ }
    }
  ]
}
```

## Query Object

### Base Query Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Query type: `select`, `aggregate`, `union`, `cte` |
| `table` | string | Yes | Primary table name |
| `alias` | string | No | Table alias (e.g., "n" for neighbourhoods) |
| `columns` | array | Yes | List of column objects to select |
| `filters` | array | No | List of filter objects (WHERE conditions) |
| `spatial_filters` | array | No | List of spatial filter objects |
| `joins` | array | No | List of join objects |
| `group_by` | array | No | List of column names to group by |
| `order_by` | array | No | List of order objects |
| `limit` | integer | No | Maximum number of results |
| `distinct` | boolean | No | Whether to use SELECT DISTINCT (default: false) |

### Column Object

```json
{
  "name": "string",           // Column name (with table prefix if joins present)
  "alias": "string",          // Optional alias for display
  "expression": "string",     // Optional SQL expression (for computed columns)
  "aggregate": "string",      // Optional: sum, count, avg, min, max, stddev
  "format": "string"          // Optional: format function (e.g., "to_char(...)")
}
```

**Important:** When a query includes joins, column names **MUST** include explicit table prefixes (e.g., `"s.name"`, `"fs.address"`) to avoid ambiguous column references. For queries without joins, simple column names are sufficient.

**Examples:**
```json
// Simple column (no joins)
{"name": "name"}

// Column with table prefix (required when joins present)
{"name": "s.name"}

// Column with table prefix and alias
{"name": "fs.station_no", "alias": "fire_station_no"}

// Column with alias (no joins)
{"name": "ward_id", "alias": "ward_identifier"}

// Geometry column (always required)
{"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}

// Geometry with table prefix in expression (joins present)
{"name": "geometry", "expression": "ST_AsGeoJSON(s.geometry)", "alias": "geometry"}

// Computed spatial column
{"name": "length", "expression": "ST_Length(geometry::geography)", "alias": "length_m"}

// Formatted computed column
{"name": "length", "expression": "to_char(ST_Length(geometry::geography), 'FM999,999,999.99')", "alias": "length_m"}

// Aggregate column
{"name": "area", "aggregate": "sum", "expression": "ST_Area(pl.geometry::geography)", "alias": "total_area_m2"}
```

### Filter Object

```json
{
  "column": "string",         // Column name
  "operator": "string",       // <, <=, >, >=, =, !=, ILIKE, NOT ILIKE, BETWEEN, IN, IS NULL, etc.
  "value": "any",            // Filter value (can be string, number, array, null)
  "logic": "AND|OR"          // Logical operator to combine with previous filter (default: AND)
}
```

**Examples:**
```json
// Simple comparison
{"column": "year_built", "operator": "<", "value": 1980}

// Text pattern matching (always use ILIKE with wildcards)
{"column": "lane_type", "operator": "ILIKE", "value": "%protected%"}

// Logical combination
{"column": "lane_type", "operator": "ILIKE", "value": "%protected%"},
{"column": "installed_year", "operator": ">=", "value": 2020, "logic": "AND"}

// IN operator
{"column": "school_type", "operator": "IN", "value": ["EP", "ES"]}

// NULL check
{"column": "amenities", "operator": "IS NOT NULL"}
```

### Spatial Filter Object

```json
{
  "operation": "string",      // ST_DWithin, ST_Intersects, ST_Contains, ST_Within
  "target_table": "string",   // Table to filter against
  "distance": "number",       // Distance in meters (for ST_DWithin)
  "use_exists": "boolean",    // Use EXISTS subquery (default: true, more efficient)
  "target_filters": "array"   // Optional: Array of filter objects to apply to target table
}
```

**Examples:**
```json
// Distance-based filter
{
  "operation": "ST_DWithin",
  "target_table": "schools",
  "distance": 500,
  "use_exists": true
}

// Intersection filter
{
  "operation": "ST_Intersects",
  "target_table": "neighbourhoods",
  "use_exists": true
}

// Spatial filter with target table filtering (single condition)
{
  "operation": "ST_DWithin",
  "target_table": "schools",
  "distance": 500,
  "use_exists": true,
  "target_filters": [
    {"column": "school_type", "operator": "=", "value": "PR"}
  ]
}

// Spatial filter with multiple target table conditions
{
  "operation": "ST_Intersects",
  "target_table": "neighbourhoods",
  "use_exists": true,
  "target_filters": [
    {"column": "area_name", "operator": "ILIKE", "value": "%north%"},
    {"column": "area_m2", "operator": ">", "value": 1000000, "logic": "AND"}
  ]
}
```

**Note:** The `target_filters` field allows filtering the target table within the spatial EXISTS subquery. This is more efficient than using a JOIN when you only need to filter the primary table based on spatial relationships with filtered target records. Each filter object in the array follows the same structure as regular filter objects (see Filter Object section).

### Join Object

```json
{
  "type": "string",          // INNER, LEFT, RIGHT, FULL
  "table": "string",         // Table to join
  "alias": "string",         // Table alias
  "condition": {
    "type": "spatial|attribute",
    "operation": "string",   // For spatial: ST_DWithin, ST_Intersects, etc.
    "left_column": "string", // For attribute joins
    "right_column": "string",// For attribute joins
    "distance": "number"     // For spatial joins with ST_DWithin
  }
}
```

**Examples:**
```json
// Spatial join
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

// Attribute join
{
  "type": "INNER",
  "table": "wards",
  "alias": "w",
  "condition": {
    "type": "attribute",
    "left_column": "ward_id",
    "right_column": "ward_id"
  }
}
```

### Order Object

```json
{
  "column": "string",        // Column name or expression
  "direction": "ASC|DESC",   // Sort direction
  "expression": "string"     // Optional: SQL expression for computed ordering
}
```

**Examples:**
```json
// Simple ordering
{"column": "name", "direction": "ASC"}

// Order by computed value
{"expression": "ST_Length(geometry::geography)", "direction": "DESC"}
```

## Advanced Query Types

### CTE (Common Table Expression) Query

```json
{
  "type": "cte",
  "ctes": [
    {
      "name": "string",      // CTE name
      "query": { /* Query Object */ }
    }
  ],
  "main_query": { /* Query Object */ }
}
```

### Union Query

```json
{
  "type": "union",
  "union_type": "ALL|DISTINCT",  // Default: ALL
  "queries": [
    { /* Query Object */ },
    { /* Query Object */ }
  ]
}
```

## Complete Examples

### Example 1: Simple Select
**User Query:** "Show all attractions"

```json
{
  "layers": [
    {
      "layer_name": "attractions",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "attractions",
        "columns": [
          {"name": "name"},
          {"name": "category"},
          {"name": "address"},
          {"name": "description"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ]
      }
    }
  ]
}
```

### Example 2: Filtered Query
**User Query:** "Get all fire stations built before 1980"

```json
{
  "layers": [
    {
      "layer_name": "fire_stations_pre_1980",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "fire_stations",
        "columns": [
          {"name": "station_no"},
          {"name": "address"},
          {"name": "year_built"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ],
        "filters": [
          {"column": "year_built", "operator": "<", "value": 1980}
        ]
      }
    }
  ]
}
```

### Example 3: Spatial Filter with Context Layer
**User Query:** "Show bike lanes within 500m of schools"

```json
{
  "layers": [
    {
      "layer_name": "bike_lanes_near_schools",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "bike_lanes",
        "distinct": true,
        "columns": [
          {"name": "street_name"},
          {"name": "lane_type"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ],
        "spatial_filters": [
          {
            "operation": "ST_DWithin",
            "target_table": "schools",
            "distance": 500,
            "use_exists": true
          }
        ]
      }
    },
    {
      "layer_name": "schools",
      "layer_type": "context",
      "query": {
        "type": "select",
        "table": "schools",
        "distinct": true,
        "columns": [
          {"name": "name"},
          {"name": "school_type_desc"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ]
      }
    }
  ]
}
```

### Example 4: Spatial Join
**User Query:** "List each school and the nearest fire station within 1 kilometer"

```json
{
  "layers": [
    {
      "layer_name": "schools_with_fire_stations",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "schools",
        "alias": "s",
        "distinct": true,
        "columns": [
          {"name": "s.name", "alias": "school_name"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(s.geometry)", "alias": "geometry"},
          {"name": "fs.station_no", "alias": "fire_station_no"},
          {"name": "fs.address", "alias": "fire_station_address"},
          {"name": "fs.municipality"}
        ],
        "joins": [
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
        ]
      }
    }
  ]
}
```

### Example 5: Aggregation with Context Layer
**User Query:** "Total parking lot area within each neighbourhood"

```json
{
  "layers": [
    {
      "layer_name": "neighbourhoods_parking_summary",
      "layer_type": "primary",
      "query": {
        "type": "aggregate",
        "table": "neighbourhoods",
        "alias": "n",
        "columns": [
          {"name": "n.id", "alias": "neighbourhood_id"},
          {"name": "n.area_name"},
          {
            "name": "total_parking_area_m2",
            "aggregate": "sum",
            "expression": "ST_Area(pl.geometry::geography)"
          },
          {"name": "geometry", "expression": "ST_AsGeoJSON(n.geometry)", "alias": "geometry"}
        ],
        "joins": [
          {
            "type": "INNER",
            "table": "parking_lots",
            "alias": "pl",
            "condition": {
              "type": "spatial",
              "operation": "ST_Intersects"
            }
          }
        ],
        "group_by": ["n.id", "n.area_name", "n.geometry"]
      }
    },
    {
      "layer_name": "parking_lots",
      "layer_type": "reference",
      "query": {
        "type": "select",
        "table": "parking_lots",
        "columns": [
          {"name": "id"},
          {"name": "last_updated"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ]
      }
    }
  ]
}
```

### Example 6: CTE Query
**User Query:** "Show neighbourhoods with more than 10 parks"

```json
{
  "layers": [
    {
      "layer_name": "neighbourhoods_with_many_parks",
      "layer_type": "primary",
      "query": {
        "type": "cte",
        "ctes": [
          {
            "name": "park_counts",
            "query": {
              "type": "aggregate",
              "table": "parks",
              "alias": "p",
              "columns": [
                {"name": "n.area_name"},
                {"name": "n.geometry"},
                {"name": "park_count", "aggregate": "count", "expression": "*"}
              ],
              "joins": [
                {
                  "type": "INNER",
                  "table": "neighbourhoods",
                  "alias": "n",
                  "condition": {
                    "type": "spatial",
                    "operation": "ST_Intersects"
                  }
                }
              ],
              "group_by": ["n.area_name", "n.geometry"]
            }
          }
        ],
        "main_query": {
          "type": "select",
          "table": "park_counts",
          "alias": "pc",
          "columns": [
            {"name": "pc.area_name"},
            {"name": "pc.park_count"},
            {"name": "geometry", "expression": "ST_AsGeoJSON(pc.geometry)", "alias": "geometry"}
          ],
          "filters": [
            {"column": "park_count", "operator": ">", "value": 10}
          ]
        }
      }
    }
  ]
}
```

### Example 7: UNION Query
**User Query:** "Merge all emergency service locations into one layer"

```json
{
  "layers": [
    {
      "layer_name": "emergency_services",
      "layer_type": "primary",
      "query": {
        "type": "union",
        "union_type": "ALL",
        "queries": [
          {
            "type": "select",
            "table": "fire_stations",
            "alias": "fs",
            "columns": [
              {"name": "fs.address", "alias": "location"},
              {"name": "service_type", "expression": "'Fire Station'"},
              {"name": "identifier", "expression": "CAST(fs.station_no AS text)"},
              {"name": "geometry", "expression": "ST_AsGeoJSON(fs.geometry)", "alias": "geometry"}
            ]
          },
          {
            "type": "select",
            "table": "police_stations",
            "alias": "ps",
            "columns": [
              {"name": "ps.address", "alias": "location"},
              {"name": "service_type", "expression": "'Police Station'"},
              {"name": "identifier", "expression": "ps.name"},
              {"name": "geometry", "expression": "ST_AsGeoJSON(ps.geometry)", "alias": "geometry"}
            ]
          },
          {
            "type": "select",
            "table": "ambulance_stations",
            "alias": "ems",
            "columns": [
              {"name": "ems.address", "alias": "location"},
              {"name": "service_type", "expression": "'Ambulance Station'"},
              {"name": "identifier", "expression": "ems.ems_name"},
              {"name": "geometry", "expression": "ST_AsGeoJSON(ems.geometry)", "alias": "geometry"}
            ]
          }
        ]
      }
    }
  ]
}
```

### Example 8: Multiple Filters with Logic
**User Query:** "Show protected bike lanes installed since 2020"

```json
{
  "layers": [
    {
      "layer_name": "protected_bike_lanes_2020_plus",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "bike_lanes",
        "columns": [
          {"name": "street_name"},
          {"name": "lane_type"},
          {"name": "installed_year"},
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ],
        "filters": [
          {"column": "lane_type", "operator": "ILIKE", "value": "%protected%"},
          {"column": "installed_year", "operator": ">=", "value": 2020, "logic": "AND"}
        ]
      }
    }
  ]
}
```

### Example 9: ORDER and LIMIT
**User Query:** "Show the 5 longest bike lanes"

```json
{
  "layers": [
    {
      "layer_name": "longest_bike_lanes",
      "layer_type": "primary",
      "query": {
        "type": "select",
        "table": "bike_lanes",
        "columns": [
          {"name": "street_name"},
          {"name": "from_street"},
          {"name": "to_street"},
          {
            "name": "bike_lanes_length_m",
            "expression": "to_char(ST_Length(geometry::geography), 'FM999,999,999.99')"
          },
          {"name": "geometry", "expression": "ST_AsGeoJSON(geometry)", "alias": "geometry"}
        ],
        "order_by": [
          {"expression": "ST_Length(geometry::geography)", "direction": "DESC"}
        ],
        "limit": 5
      }
    }
  ]
}
```

## Table Disambiguation in Joins

When a query includes JOIN clauses, **all column references in the `columns` array MUST include explicit table prefixes** to avoid ambiguous column errors. This is critical because multiple tables in a join may have columns with the same name (e.g., both `schools` and `fire_stations` may have an `address` column).

### Rules for Column Naming

1. **Queries WITHOUT joins**: Simple column names are acceptable
   - Example: `{"name": "address"}`

2. **Queries WITH joins**: All columns must include table prefixes
   - Example: `{"name": "fs.address"}`
   - Use the table alias if one is specified
   - Even if a column appears to be unique, use the prefix for consistency

3. **Expressions**: When using SQL expressions, include table prefixes in the expression
   - Example: `{"expression": "ST_AsGeoJSON(s.geometry)", "alias": "geometry"}`

### Examples

**❌ INCORRECT** (will cause "column does not exist" errors):
```json
{
  "table": "schools",
  "alias": "s",
  "joins": [{"table": "fire_stations", "alias": "fs", ...}],
  "columns": [
    {"name": "name", "alias": "school_name"},
    {"name": "address", "alias": "fire_station_address"}  // Ambiguous!
  ]
}
```

**✅ CORRECT**:
```json
{
  "table": "schools",
  "alias": "s",
  "joins": [{"table": "fire_stations", "alias": "fs", ...}],
  "columns": [
    {"name": "s.name", "alias": "school_name"},
    {"name": "fs.address", "alias": "fire_station_address"}
  ]
}
```

## Design Principles

1. **Explicitness**: All SQL operations should be explicitly represented in the JSON structure
2. **Geometry Required**: Every layer must include geometry output as `ST_AsGeoJSON(geometry)`
3. **Context Layers**: LLM should explicitly define context layers when spatial filtering or joining
4. **Type Safety**: Use appropriate types (numbers for distances, arrays for IN operations, etc.)
5. **Consistency**: Use consistent naming (snake_case for database elements, camelCase for JSON)
6. **Table Disambiguation**: When joins are present, all column names must include table prefixes
7. **Extensibility**: Structure allows for future additions without breaking existing functionality

## Validation Requirements

The query_builder assumes the following validations have been performed:
- All referenced tables exist in the schema
- All referenced columns exist in their respective tables
- Spatial operations use appropriate geometry types
- Aggregate functions are only used with GROUP BY when appropriate
- Filter values match column data types