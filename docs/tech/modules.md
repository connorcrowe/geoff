# Module Reference

**Purpose**: Quick reference for all backend modules with interfaces, dependencies, and implementation details.

---

## Module Catalog

| Module | Purpose | Key Input | Key Output | Dependencies |
|--------|---------|-----------|------------|--------------|
| **Core Pipeline** |
| [`query_service`](../../backend/services/query_service.py:1) | Orchestrates end-to-end query pipeline | User query text | Layers (GeoJSON + tabular) | llm, query_builder, parse_results, vector_db, embed, prompt_builder |
| **LLM Integration** |
| [`llm`](../../backend/core/llm.py:1) | Generate JSON plans from natural language | Formatted prompt | JSON plan dict | OpenAI API |
| [`prompt_builder`](../../backend/core/prompt_builder.py:1) | Assemble prompts with context | Schema + examples + query | Formatted prompt string | None |
| **Query Processing** |
| [`query_builder`](../../backend/core/query_builder.py:1) | Convert JSON plan to SQL | JSON plan dict | List of SQL strings | None |
| [`parse_results`](../../backend/core/parse_results.py:1) | Execute SQL and format results | List of SQL queries | List of layer objects | db |
| **Data Access** |
| [`db`](../../backend/db/db.py:1) | Execute SQL against PostgreSQL | SQL string | List of dict rows | psycopg2 |
| [`vector_db`](../../backend/db/vector_db.py:1) | Semantic search via embeddings | Query embedding vector | Relevant tables/examples | db |
| **Utilities** |
| [`embed`](../../backend/utils/embed.py:1) | Generate text embeddings | Text string | 1536-dim vector | OpenAI API |
| [`geo`](../../backend/core/geo.py:1) | Convert WKB to GeoJSON | SQL rows + column names | Layer objects | shapely |
| **API** |
| [`routes`](../../backend/api/routes.py:1) | REST API endpoints | HTTP requests | JSON responses | query_service, db |

---

## Detailed Module Specifications

### Query Service ⭐ Orchestrator

**Location**: [`backend/services/query_service.py`](../../backend/services/query_service.py:1)

**Purpose**: Coordinates the entire query pipeline from natural language input to map-ready output.

**Main Function**: `handle_user_query(user_question: str, retries: int = 2)`

**Process Flow**:
```
User Query → Embed → Vector Search → Prompt Building → LLM → JSON Plan → SQL Generation → Execution → Layers
```

**Input**:
- `user_question` (str): Natural language query from user
- `retries` (int): Number of retry attempts on failure

**Output** (dict):
```python
{
    "sql": "",  # Currently empty, preserved for compatibility
    "layers": [...],  # List of layer objects (see parse_results)
    "error": None  # Error message if failed
}
```

**Pipeline Steps**:
1. **Embed**: Convert query to vector using [`embed.embed_text()`](../../backend/utils/embed.py:11)
2. **Retrieve Context**: Get relevant tables and examples via [`vector_db`](../../backend/db/vector_db.py:1)
3. **Build Prompt**: Format schema and examples via [`prompt_builder`](../../backend/core/prompt_builder.py:1)
4. **Generate Plan**: Call LLM via [`llm.generate_json_plan()`](../../backend/core/llm.py:58)
5. **Build SQL**: Convert plan to queries via [`query_builder.build_query()`](../../backend/core/query_builder.py:5)
6. **Execute & Format**: Run queries and create layers via [`parse_results()`](../../backend/core/parse_results.py:17)

**Logging**:
- Logs to `logs/query_service.log`
- Tracks: request_id, user_question, duration, status
- Useful for debugging and monitoring

**Error Handling**:
- Retry logic: Will retry `retries` times on failure
- Currently returns error in response dict

**Testing**: Integration testing via API calls

**Dependencies**:
- **Used by**: [`routes.py`](../../backend/api/routes.py:1)
- **Depends on**: All core modules (orchestrator role)

---

### Query Builder ⭐ Complex

**Location**: [`backend/core/query_builder.py`](../../backend/core/query_builder.py:1)

**Purpose**: Converts structured JSON plans into executable PostGIS SQL queries.

**Main Function**: `build_query(plan: Dict) -> List[str]`

**Interface**:
- **Input**: JSON plan dict (see [`../specs/json_plan.md`](../specs/json_plan.md))
- **Output**: List of SQL query strings (one per layer)

**Supported Query Types**:
- **SELECT**: Standard queries with filters
- **AGGREGATE**: Queries with GROUP BY and aggregate functions (SUM, COUNT, AVG, MIN, MAX, STDDEV)
- **UNION**: Merge multiple queries with UNION or UNION ALL
- **CTE**: Common Table Expressions (WITH clauses) for complex queries

**Supported Query Patterns**:

1. **Simple SELECT** - Filtering and sorting
```sql
SELECT col1, col2, ST_AsGeoJSON(geometry) AS geometry
FROM table
WHERE condition
ORDER BY col1 DESC
LIMIT 10
```

2. **Spatial Filter (EXISTS)** - Items near other features
```sql
SELECT DISTINCT t1.*, ST_AsGeoJSON(t1.geometry) AS geometry
FROM table1 t1
WHERE EXISTS (
    SELECT 1 FROM table2 t2
    WHERE ST_DWithin(t1.geometry::geography, t2.geometry::geography, 500)
)
```

3. **Spatial Join** - Pairwise spatial relationships
```sql
SELECT DISTINCT t1.col1, t2.col2, ST_AsGeoJSON(t1.geometry) AS geometry
FROM table1 t1
INNER JOIN table2 t2 ON ST_Intersects(t1.geometry, t2.geometry)
```

4. **Attribute Join** - Join on non-spatial columns
```sql
SELECT t1.*, t2.data, ST_AsGeoJSON(t1.geometry) AS geometry
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.foreign_id
```

5. **Aggregation** - GROUP BY with aggregate functions
```sql
SELECT n.name, SUM(ST_Area(p.geometry::geography)) AS total_area,
       ST_AsGeoJSON(n.geometry) AS geometry
FROM neighbourhoods n
JOIN parcels p ON ST_Intersects(n.geometry, p.geometry)
GROUP BY n.name, n.geometry
```

6. **CTE Query** - Complex queries with WITH clauses
```sql
WITH filtered AS (
    SELECT * FROM table WHERE condition
)
SELECT f.col1, ST_AsGeoJSON(f.geometry) AS geometry
FROM filtered f
WHERE f.col2 > 100
```

7. **UNION Query** - Merge multiple datasets
```sql
SELECT 'Fire' AS type, address, ST_AsGeoJSON(geometry) AS geometry FROM fire_stations
UNION ALL
SELECT 'Police' AS type, address, ST_AsGeoJSON(geometry) AS geometry FROM police_stations
```

**Supported Features**:
- **Spatial Operations**: ST_DWithin, ST_Intersects, ST_Contains, ST_Within
- **Spatial Functions**: ST_Area, ST_Length, ST_Centroid, ST_Perimeter
- **Aggregate Functions**: SUM, COUNT, AVG, MIN, MAX, STDDEV
- **Filter Operators**: <, <=, >, >=, =, !=, ILIKE, BETWEEN, IN, IS NULL, IS NOT NULL
- **Logical Operators**: AND, OR
- **Computed Columns**: SQL expressions with formatting (to_char)
- **Join Types**: INNER, LEFT, RIGHT, FULL
- **Query Clauses**: WHERE, GROUP BY, ORDER BY, LIMIT, DISTINCT

**Table Disambiguation**:
- **Critical**: When queries include JOINs, all column names in the JSON plan **must** include explicit table prefixes (e.g., `"s.name"`, `"fs.address"`)
- This prevents ambiguous column reference errors when multiple tables have columns with the same name
- See [`../specs/json_plan.md`](../specs/json_plan.md) for detailed examples

**Key Design Choices**:
- **No automatic prefixing**: Column names used exactly as specified in JSON plan
- **Explicit disambiguation**: JSON plan responsible for table prefixes in joins
- **Geography casting**: Uses `::geography` for distance operations (meters)
- **GeoJSON output**: All geometry columns converted via `ST_AsGeoJSON()`

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1), [`parse_results`](../../backend/core/parse_results.py:1)
- **Depends on**: None (pure function)

---

### Parse Results

**Location**: [`backend/core/parse_results.py`](../../backend/core/parse_results.py:1)

**Purpose**: Executes SQL queries and converts results into map-ready layer format.

**Main Function**: `parse_results(queries: List[str]) -> List[dict]`

**Interface**:
- **Input**: List of SQL query strings
- **Output**: List of layer objects

**Layer Object Structure**:
```python
{
    "name": "table_name",  # Extracted from SQL FROM clause
    "geojson": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {...},  # GeoJSON geometry
                "properties": {...}  # Non-geometry attributes
            }
        ]
    },
    "columns": ["col1", "col2"],  # Non-geometry column names
    "rows": [[val1, val2], ...]  # Tabular data for ResultsPanel
}
```

**Process**:
1. Execute each query via [`db.execute_sql()`](../../backend/db/db.py:14)
2. Detect geometry column via `_detect_geom_col()`
3. Separate geometry from properties
4. Build GeoJSON FeatureCollection
5. Extract layer name from SQL query
6. Return list of layers

**Key Functions**:
- `_detect_geom_col(row)`: Finds geometry column by checking for GeoJSON structure

**Features**:
- **Automatic geometry detection**: Finds geometry column even if not named "geometry"
- **Dual output format**: GeoJSON for map + tabular data for table view
- **Layer naming**: Extracts table name from SQL query for labeling

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1)
- **Depends on**: [`db.execute_sql()`](../../backend/db/db.py:14)

---

### Vector DB ⭐ Important

**Location**: [`backend/db/vector_db.py`](../../backend/db/vector_db.py:1)

**Purpose**: Performs semantic search to retrieve relevant database schemas and example queries.

**Main Functions**:

#### `select_relevant_tables(embedding, score_threshold=-0.3)`
Finds database tables/columns relevant to the query.

**Input**:
- `embedding`: 1536-dim query embedding vector
- `score_threshold`: Cosine similarity cutoff (default: -0.3)

**Output**:
```python
[
    {
        "table_name": "bike_lanes",
        "columns": [
            {
                "column_name": "street_name",
                "col_type": "text",
                "description": "Primary street name..."
            }
        ]
    }
]
```

**Process**:
1. Query `meta.schema_embeddings` table with cosine similarity
2. Filter by similarity threshold
3. Group columns by table
4. Sort tables by best column match

#### `select_relevant_examples(embedding, score_threshold=-0.3)`
Finds example query/plan pairs similar to the user's query.

**Input**:
- `embedding`: 1536-dim query embedding vector
- `score_threshold`: Cosine similarity cutoff (default: -0.3)

**Output**:
```python
[
    {
        "id": 1,
        "type": "spatial_filter",
        "sources": ["bike_lanes", "schools"],
        "user_query": "Show bike lanes near schools",
        "plan": {...},  # Full JSON plan
        "score": -0.45
    }
]
```

**Database Tables**:
- `meta.schema_embeddings`: Table/column descriptions with embeddings
- `meta.example_embeddings`: Example query/plan pairs with embeddings

**Similarity Metric**:
- Uses negative inner product operator `<#>` for cosine similarity
- Lower (more negative) scores = more similar
- Threshold of -0.3 means >0.3 cosine similarity

**Key Limitation**:
- ⚠️ **Fixed threshold**: -0.3 threshold may not be optimal for all queries
- ⚠️ **No dynamic adjustment**: Doesn't adjust retrieval based on result count

**Testing**: Manual testing only (no automated tests yet)

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1)
- **Depends on**: [`db.execute_sql()`](../../backend/db/db.py:14)

---

### LLM Integration

**Location**: [`backend/core/llm.py`](../../backend/core/llm.py:1)

**Purpose**: Interfaces with OpenAI API to generate structured JSON plans from natural language.

**Main Function**: `generate_json_plan(prompt: str) -> dict`

**Interface**:
- **Input**: Formatted prompt string (from [`prompt_builder`](../../backend/core/prompt_builder.py:1))
- **Output**: JSON plan as Python dict

**Configuration**:
- **Model**: GPT-4o-mini
- **Temperature**: 0 (deterministic output)
- **Max tokens**: 1024

**Process**:
1. Send prompt to OpenAI Chat Completions API
2. Parse response, strip markdown code fences
3. Convert JSON string to Python dict
4. Return structured plan

**Output Cleaning**:
- Strips markdown code fences (backticks)
- Removes "json" language identifier
- Converts single quotes to double quotes
- Parses to dict via `json.loads()`

**Error Handling**:
- Raises HTTP errors from API calls
- May raise JSON parse errors if response malformed

**Legacy Function**:
- `generate_sql(prompt)`: Direct NL→SQL generation (deprecated, not used)

**Testing**: Integration testing via query pipeline

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1)
- **Depends on**: OpenAI API, [`prompt_builder`](../../backend/core/prompt_builder.py:1) (indirectly)

---

### Prompt Builder

**Location**: [`backend/core/prompt_builder.py`](../../backend/core/prompt_builder.py:1)

**Purpose**: Constructs formatted prompts for LLM with schema context and examples.

**Functions**:

#### `build_schema_prompt(relevant_tables)`
Formats table schemas as text for LLM context.

**Input**: List of table objects from [`vector_db.select_relevant_tables()`](../../backend/db/vector_db.py:39)

**Output**:
```
Table: bike_lanes
  - street_name (text): Primary street name where the bike lane is located
  - geometry (geometry): Geometry: line segment of the bike lane

Table: schools
  - name (text): Name of the school
  - geometry (geometry): Geometry: point location of the school
```

#### `build_examples_prompt(relevant_examples, n=5)`
Formats example query/plan pairs for few-shot learning.

**Input**: 
- `relevant_examples`: List from [`vector_db.select_relevant_examples()`](../../backend/db/vector_db.py:5)
- `n`: Number of examples to include (default: 5)

**Output**:
```
User Query: Show bike lanes near schools
Plan:
{...JSON plan...}

User Query: Show all parks
Plan:
{...JSON plan...}
```

#### `build_full_prompt(user_question, schema_text, examples_text, ...)`
Assembles complete prompt with user query, schema, and examples.

**Note**: This function exists but is **not currently used** in the pipeline. The LLM receives prompts directly through the system message in [`llm.py`](../../backend/core/llm.py:1).

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1)
- **Depends on**: None

---

### Embedding Service

**Location**: [`backend/utils/embed.py`](../../backend/utils/embed.py:1)

**Purpose**: Generates vector embeddings for text using OpenAI API.

**Function**: `embed_text(text: str) -> List[float]`

**Interface**:
- **Input**: Text string (user query, schema description, etc.)
- **Output**: 1536-dimensional embedding vector

**Configuration**:
- **Model**: text-embedding-3-small
- **Dimensions**: 1536 (default for this model)

**Usage**: 
- Query embedding for semantic search
- Schema/example embeddings (generated via ETL)

**Testing**: Integration testing via vector search

**Dependencies**:
- **Used by**: [`query_service`](../../backend/services/query_service.py:1), ETL scripts
- **Depends on**: OpenAI API

---

### Database Service

**Location**: [`backend/db/db.py`](../../backend/db/db.py:1)

**Purpose**: Executes SQL queries against PostgreSQL database.

**Function**: `execute_sql(sql: str) -> List[dict]`

**Interface**:
- **Input**: SQL query string
- **Output**: List of row dictionaries

**Configuration**:
- Connection pool managed globally
- Search path set to: `data, public`
- Uses `psycopg2.extras.RealDictCursor` for dict-based results

**Error Handling**:
- Catches exceptions and rolls back transaction
- Returns `None` on error in some cases (inconsistent)
- Prints debug info if `DEBUG_MODE` is enabled

**Key Features**:
- **Persistent connection**: Single connection reused across requests
- **Dict cursor**: Returns rows as dicts for easier access
- **Auto-rollback**: Transaction rolled back on errors

**Known Issues**:
- ⚠️ **Inconsistent return**: Sometimes returns `None`, sometimes `None, None`
- ⚠️ **Global connection**: Not thread-safe for concurrent requests
- ⚠️ **No connection pooling**: Uses single persistent connection

**Testing**: Integration testing via query execution

**Dependencies**:
- **Used by**: All modules that access database
- **Depends on**: psycopg2, config settings

---

### Geometry Processing

**Location**: [`backend/core/geo.py`](../../backend/core/geo.py:1)

**Purpose**: Converts WKB geometry to GeoJSON and builds layer objects.

**Main Function**: `convert_to_geo_layers(rows, colnames) -> List[dict]`

**Status**: ⚠️ **Not currently used in main pipeline**. [`parse_results.py`](../../backend/core/parse_results.py:1) handles geometry conversion directly using `ST_AsGeoJSON()` in SQL.

**Interface**:
- **Input**: SQL rows (tuples) and column names
- **Output**: List of layer objects (similar to parse_results)

**Process**:
1. Identify geometry columns via WKB detection
2. For each geometry column, build a separate layer
3. Convert WKB to GeoJSON using shapely
4. Separate properties from geometry

**Key Functions**:
- `_find_geometry_columns()`: Detect geometry columns by trying WKB parsing
- `_build_layer()`: Create layer object for one geometry column
- `_convert_wkb_to_geojson()`: Convert WKB hex to GeoJSON using shapely

**Why Not Used**:
Current approach uses `ST_AsGeoJSON()` in SQL which is simpler and more efficient. This module provides an alternative for cases where geometry must be retrieved as WKB.

**Dependencies**:
- **Used by**: None currently (legacy/alternative approach)
- **Depends on**: shapely

---

### API Routes

**Location**: [`backend/api/routes.py`](../../backend/api/routes.py:1)

**Purpose**: FastAPI endpoints for frontend interaction.

**Endpoints**:

#### `POST /query`
Main query endpoint - processes natural language queries.

**Request**:
```json
{
    "prompt": "Show bike lanes near schools"
}
```

**Response**:
```json
{
    "sql": "",
    "layers": [...],
    "error": null
}
```

#### `GET /examples?limit=999`
Retrieves example queries from database.

**Response**:
```json
[
    {"user_query": "Show all bike lanes"},
    {"user_query": "Show schools in downtown"}
]
```

**Usage**: Populate autocomplete dropdown in frontend

#### `GET /schemas`
Retrieves complete database schema information.

**Response**:
```json
{
    "bike_lanes": [
        {
            "column_name": "street_name",
            "column_type": "text",
            "description": "Primary street name..."
        }
    ],
    "schools": [...]
}
```

**Usage**: Display schema in "More Info" modal in frontend

**Dependencies**:
- **Used by**: Frontend application
- **Depends on**: [`query_service`](../../backend/services/query_service.py:1), [`db`](../../backend/db/db.py:1)

---

## Module Dependency Graph

```
Frontend HTTP Request
         ↓
    routes.py
         ↓
  query_service.py (Orchestrator)
         ↓
    ┌────┴────┬──────────┬───────────┐
    ↓         ↓          ↓           ↓
 embed.py  vector_db  llm.py   query_builder.py
    ↓         ↓          ↓           ↓
    └─────→ db.py    (OpenAI)  parse_results.py
              ↑                      ↓
              └──────────────────────┘
                   
prompt_builder.py ─→ llm.py (formats context)

geo.py (alternative geometry processing, not used)
```

**Legend**:
- **Solid arrows**: Direct function calls
- **Orchestrator** (query_service): Coordinates all other modules
- **External dependencies**: OpenAI API for embeddings and LLM

---

## See Also

- **System Architecture**: [`architecture.md`](architecture.md)
- **JSON Plan Specification**: [`../json_plan.md`](../json_plan.md)
- **Database Schema**: [`data_schema.md`](data_schema.md)
- **Implementation Patterns**: Coming soon in `patterns.md`