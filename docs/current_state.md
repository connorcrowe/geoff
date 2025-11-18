# Current State

**Purpose**: High-level status of what's implemented, what's in progress, and what's not yet built. For implementation details, see [`tech/modules.md`](tech/modules.md).

---

## Implementation Status

### ✅ Fully Implemented

**Core Query Pipeline**:
- Natural language → JSON plan → SQL → Results pipeline
- Simple SELECT queries with filters
- Spatial proximity filtering (ST_DWithin, ST_Intersects, ST_Contains)
- Spatial joins (pairwise matching between geometries)
- Attribute-based joins
- Multi-layer map results (multiple geometries per question)
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
- Frontend query interface with autocomplete
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
- Limited retry logic

**Query Validation**:
- JSON plan structure assumed valid
- No validation before SQL generation
- No sanity checks on generated SQL

**Spatial Functions**:
- ST_Area and ST_Length supported in SELECT
- Other computed spatial functions not tested

### ❌ Not Yet Implemented

**Query Capabilities**:
- ❌ Aggregations (GROUP BY, COUNT, SUM, AVG, etc.)
- ❌ Computed columns / expressions in SELECT
- ❌ Complex WHERE operators (BETWEEN, NOT IN, etc.)
- ❌ CTEs (WITH clauses) or subqueries
- ❌ Multiple spatial functions per query
- ❌ UNION or INTERSECT operations

**Geometry Operations**:
- ❌ Geometry creation (buffers, unions, etc.)
- ❌ Route generation / pathfinding
- ❌ Network analysis
- ❌ Convex hulls, centroids, etc.

**Memory & Context**:
- ❌ Memory of previous queries
- ❌ Reference to previous layers
- ❌ Query history or session state
- ❌ User preferences

**Intelligence**:
- ❌ Place resolution (which neighbourhood contains which ward)
- ❌ Smart handling of place name ambiguity
- ❌ Understanding place hierarchies and relationships
- ❌ Learning from user feedback
- ❌ Query explanation to user
- ❌ Clarification questions to user

**Data & Export**:
- ❌ Data export functionality
- ❌ Share results via URL
- ❌ Save queries or results
- ❌ Custom dataset upload

---

## Module Status Summary

For detailed implementation information, see [`tech/modules.md`](tech/modules.md).

| Module | Status | Notes |
|--------|--------|-------|
| [`query_service`](tech/modules.md#query-service--orchestrator) | ✅ Production | Orchestrates full pipeline |
| [`llm`](tech/modules.md#llm-integration) | ✅ Production | OpenAI GPT-4o-mini integration |
| [`query_builder`](tech/modules.md#query-builder--complex) | ✅ Limited | Works for simple queries; no aggregations |
| [`parse_results`](tech/modules.md#parse-results) | ✅ Production | Executes and formats layers |
| [`vector_db`](tech/modules.md#vector-db--important) | ✅ Production | Semantic search working well |
| [`prompt_builder`](tech/modules.md#prompt-builder) | ✅ Production | Context assembly functional |
| [`embed`](tech/modules.md#embedding-service) | ✅ Production | OpenAI embeddings integration |
| [`db`](tech/modules.md#database-service) | ⚠️ Works | Single connection, not thread-safe |
| [`geo`](tech/modules.md#geometry-processing) | 🔵 Unused | Alternative approach, not in pipeline |
| [`routes`](tech/modules.md#api-routes) | ✅ Production | All endpoints functional |

**Legend**: ✅ Production-ready | ⚠️ Works with caveats | 🚧 In progress | 🔵 Not used | ❌ Not implemented

---

## System Capabilities

### What Geoff Can Do Today

**Query Types**:
- "Show all [dataset]"
- "Show [dataset] with [attribute filter]"
- "Show [dataset A] near [dataset B]"
- "Show [dataset A] within [distance] of [dataset B]"
- "Show [dataset A] intersecting [dataset B]"
- "Show [dataset A] joined with [dataset B] on [attribute]"

**Example Working Queries**:
```
Show all bike lanes
Show schools in downtown
Show bike lanes installed after 2020
Show bike lanes near schools
Show bike lanes within 500m of parks
Show parks and schools (multiple layers)
```

### What Geoff Cannot Do Yet

**Query Types Not Supported**:
- "Count [dataset] per [area]" (aggregation)
- "Show a 500m buffer around [dataset]" (geometry creation)
- "Find route from A to B" (routing)
- "Show [dataset] in high-income neighbourhoods" (no demographic data)
- "What did I search for earlier?" (no memory)
- "Why did you show these results?" (no explanation)

---

## Known Issues & Limitations

### Critical Limitations

1. **No Aggregations**
   - Cannot COUNT, SUM, AVG, or GROUP BY
   - Workaround: Use manual SQL queries for now
   - Impact: Many CRE and planning questions require aggregation
   - See: [`query_builder` limitations](tech/modules.md#query-builder--complex)

2. **No Geometry Creation**
   - Cannot generate buffers, unions, convex hulls, etc.
   - Workaround: Pre-compute in database or use manual queries
   - Impact: Cannot answer "show 500m around X" style questions

3. **No Memory**
   - Each query is independent
   - Cannot reference previous results
   - Impact: Cannot do multi-step analysis

4. **Limited Place Understanding**
   - Has neighbourhood and ward datasets
   - No understanding of containment or overlap relationships
   - Impact: Cannot resolve "schools in Yorkville" if Yorkville isn't explicitly in data

### Technical Debt

- **Database connection**: Single persistent connection, not thread-safe for concurrent requests
- **Error messages**: Not user-friendly, don't explain what went wrong
- **Test coverage**: No automated tests for vector_db, partial coverage elsewhere
- **Logging**: Basic logging exists but could be more structured

### Data Limitations

- **Geographic scope**: Toronto only (by design)
- **Data freshness**: Depends on update frequency of source datasets
- **Limited datasets**: Only some tables currently (see [`data_schema.md`](tech/data_schema.md))
- **No demographic data**: No census, income, or population data yet

---

## Recent Changes

*This section will track major changes as the project evolves*

**Latest**: Documentation restructure
- Created ['vision.md`](vision.md) to describe aspirational future capabilities (with `use_cases/`)
- Created [`tech/modules.md`](tech/modules.md) with detailed module specifications
- Created [`current_state.md`](current_state.md) for status-focused description of modules and capabilities
- Created [`tech/architecture.md`](tech/architecture.md) for how modules interact and data/control flow

---

## Next Steps

See [`roadmap.md`](roadmap.md) for prioritized feature development plan.

**Immediate priorities**:


---

## Architecture & Implementation

For detailed technical information:
- **System Architecture**: [`tech/architecture.md`](tech/architecture.md)
- **Module Specifications**: [`tech/modules.md`](tech/modules.md)
- **Database Schema**: [`tech/data_schema.md`](tech/data_schema.md)
- **JSON Plan Spec**: [`json_plan.md`](json_plan.md)