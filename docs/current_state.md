# Current State

**Purpose**: High-level status of what's implemented, what's in progress, and what's not yet built. For implementation details, see [`tech/modules.md`](tech/modules.md).

---

## Implementation Status

### ✅ Fully Implemented

**Core Query Pipeline**:
- Natural language → JSON plan → SQL → Results pipeline
- SELECT queries with WHERE filters (all standard operators: `<`, `<=`, `>`, `>=`, `=`, `!=`, `ILIKE`, `BETWEEN`, `IN`, `IS NULL`, etc.)
- Spatial filtering (ST_DWithin, ST_Intersects, ST_Contains, ST_Within)
- Spatial joins (pairwise matching between geometries)
- Attribute-based joins
- Aggregations (GROUP BY, COUNT, SUM, AVG, MIN, MAX, STDDEV)
- Computed columns and expressions in SELECT
- Spatial calculations (ST_Area, ST_Length, ST_Centroid, ST_Perimeter)
- CTEs (WITH clauses) and subqueries
- UNION/UNION ALL operations
- ORDER BY and LIMIT
- Multi-layer map results with automatic context layers
- GeoJSON output for map visualization
- Tabular data output for results panel

**RAG System**:
- Vector embedding generation (OpenAI text-embedding-3-small)
- Semantic search for relevant database schemas
- Semantic search for relevant example queries
- Few-shot learning with example database
- Context-aware prompt construction

**API & Frontend Integration**:
- REST API endpoints (`/query`, `/examples`, `/schemas`)
- Frontend query interface
- Interactive map with multiple layers
- Synchronized results table and map selection

**Data**:
- 10 core datasets loaded (see [`tech/data_schema.md`](tech/data_schema.md))
- Schema embeddings for all tables/columns
- Example query embeddings for common patterns

### 🚧 Partially Implemented

**Error Handling**:
- Basic error catching exists
- Inconsistent error messages to user
- No detailed failure explanations

**Query Validation**:
- JSON plan structure assumed valid
- No validation before SQL generation
- No sanity checks on generated SQL

### ❌ Not Yet Implemented

**Geometry Operations**:
- Geometry creation (buffers, boundary generation, etc.)
- Route generation / pathfinding
- Network analysis

**Memory & Context**:
- Memory of previous queries
- Reference to previous layers
- User preferences

**Transparency**:
- Query explanation to user
- Clarification questions to user

**Intelligence**:
- Place resolution (which neighbourhood contains which ward)
- Smart handling of place name ambiguity
- Understanding place hierarchies and relationships
- Learning from user feedback

**Data & Export**:
- Data export/share functionality
- Save queries or results
- Custom dataset upload

---

## Module Status Summary

For detailed implementation information, see [`tech/modules.md`](tech/modules.md).

| Module | Status | Notes |
|--------|--------|-------|
| [`query_service`](tech/modules.md#query-service--orchestrator) | ✅ Production | Orchestrates full pipeline |
| [`llm`](tech/modules.md#llm-integration) | ✅ Production | OpenAI GPT-4o-mini integration |
| [`query_builder`](tech/modules.md#query-builder--complex) | ✅ Production | Full SQL feature set including aggregations |
| [`parse_results`](tech/modules.md#parse-results) | ✅ Production | Executes and formats layers |
| [`vector_db`](tech/modules.md#vector-db--important) | ✅ Production | Semantic search working well |
| [`prompt_builder`](tech/modules.md#prompt-builder) | ✅ Production | Context assembly functional |
| [`embed`](tech/modules.md#embedding-service) | ✅ Production | OpenAI embeddings integration |
| [`db`](tech/modules.md#database-service) | ⚠️ Works | Single connection, not thread-safe |
| [`routes`](tech/modules.md#api-routes) | ✅ Production | All endpoints functional |

---

## System Capabilities

### What Geoff Can Do Today

For a more technical breakdown of the types of SQL queries Geoff can construct, see the JSON plan specification, [`specs/json_plan.md`](specs/json_plan.md).

**Query Types**:
- "Show all [dataset]"
- "Show [dataset] with [attribute filter]"
- "Show [dataset A] near [dataset B]"
- "Show [dataset A] within [distance] of [dataset B]"
- "Show [dataset A] intersecting [dataset B]"
- "Show [dataset A] joined with [dataset B] on [attribute]"
- "Count [dataset] per [area]" (aggregation)
- "Show top N [dataset] by [measure]" (ORDER BY + LIMIT)
- "Merge [dataset A] and [dataset B]" (UNION)

**Example Working Queries**:
```
Show all bike lanes
Show schools in downtown
Show bike lanes installed after 2020
Show bike lanes near schools
Show bike lanes within 500m of parks
Show parks and schools (multiple layers)
Count schools per neighbourhood
Show the 5 longest bike lanes
Total parking lot area within each neighbourhood
How many schools are within 500m of a park?
Merge all emergency service locations into one layer
```

### What Geoff Cannot Do Yet

**Query Types Not Supported**:
- "Show a 500m buffer around [dataset]" (geometry creation)
- "Find route from A to B" (routing)
- "Show [dataset] in high-income neighbourhoods" (no demographic data)
- "What did I search for earlier?" (no memory)
- "Why did you show these results?" (no explanation)

---

## Known Issues & Limitations

### Critical Limitations

1. **No Geometry Creation**
   - Cannot generate buffers, unions, convex hulls, etc.
   - Impact: Cannot answer "show 500m around X" style questions

2. **No Memory**
   - Each query is independent
   - Cannot reference previous results
   - Impact: Cannot do multi-step analysis

3. **Limited Place Understanding**
   - No understanding of containment or overlap relationships
   - Impact: Cannot resolve "schools in Yorkville" if Yorkville isn't explicitly in data

### Technical Debt

- **Database connection**: Critical. Single persistent connection, not thread-safe for concurrent requests
- **Error messages**: Not user-friendly, don't explain what went wrong
- **Test coverage**: No automated tests for `vector_db`, partial coverage elsewhere
- **Logging**: Basic logging exists but could be more structured

### Data Limitations

- **Geographic scope**: Toronto only (by design)
- **Data freshness**: Depends on update frequency of source datasets
- **Limited datasets**: Only some tables currently (see [`data_schema.md`](tech/data_schema.md))
- **No demographic data**: No census, income, or population data yet

---

## Recent Changes

See [`CHANGELOG.md`](CHANGELOG.md) for detailed project history, short summaries in [README.md](../README.md).

---

## Next Steps

See [`roadmap.md`](roadmap.md) for prioritized feature development plan.

## Architecture & Implementation

For detailed technical information:
- **System Architecture**: [`tech/architecture.md`](tech/architecture.md)
- **Module Specifications**: [`tech/modules.md`](tech/modules.md)
- **Database Schema**: [`tech/data_schema.md`](tech/data_schema.md)
- **JSON Plan Spec**: [`json_plan.md`](specs/json_plan.md)