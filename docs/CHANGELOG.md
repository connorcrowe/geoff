# Changelog

All notable changes to the Geoff project will be documented in this file.

As per [Semantic Versioning](https://semver.org/spec/v2.0.0.html) Geoff is an initial development (0.*.*). All changes may break backwards compatibility at this time.

## [Unreleased]

- 

## [2025-11-24] - 0.3.1 - Spatial Filter Fix, Add Building, Zoning and Transit Stop datasets

### Added
- `target_filters` support in spatial filter objects - allows filtering the target table within spatial EXISTS subqueries
  - Supports array of filter conditions to apply to the target table
  - More efficient than JOINs for filtering without needing target table columns
- Building outlines dataset added to ETL pipeline
- Transit stops dataset added to ETL pipeline (from GTFS data)
- Zoning dataset added to ETL pipeline with zone types, unit limits, and exceptions
- Added 21 new example queries (044-064) demonstrating building outlines, transit stops, and zoning datasets usage

### Changed
- Enhanced spatial filter functionality in query builder to support complex target table filtering
- Updated example 003.json to use new `target_filters` array format

### Documentation
- Updated [`docs/specs/json_plan.md`](docs/specs/json_plan.md) with `target_filters` specification
- Updated [`docs/specs/query_builder.md`](docs/specs/query_builder.md) with spatial filter examples using target filters

## [2025-11-21] - 0.3.0 - Query Builder Enhancement

### Added
- Full GROUP BY support with aggregation functions (COUNT, SUM, AVG, MIN, MAX, STDDEV)
- CTEs (WITH clauses) support for complex queries
- Subquery support in SQL generation
- UNION and UNION ALL operations for combining result sets
- Computed columns and complex expressions in SELECT clauses
- Advanced WHERE operators: BETWEEN, IN, IS NULL
- Spatial calculation functions in SELECT: ST_Area, ST_Length, ST_Centroid, ST_Perimeter
- ORDER BY and LIMIT clauses for sorting and pagination
- Automatic generation of context layers for certain spatial operations

### Changed
- Enhanced query builder module with comprehensive SQL feature set
- Improved spatial query capabilities

### Documentation
- Full specification documented in [`specs/query_builder.md`](specs/query_builder.md)

## [2025-11-19] - 0.2.1 - Start Documentation

### Added
- [`vision.md`](vision.md) - Aspirational future capabilities and vision
- [`use_cases/`](use_cases/) directory - Real-world usage scenarios
- [`tech/modules.md`](tech/modules.md) - Detailed module specifications
- [`current_state.md`](current_state.md) - Status-focused module and capability descriptions
- [`tech/architecture.md`](tech/architecture.md) - Module interactions and data/control flow

### Changed
- Reorganized documentation structure for better clarity and maintainability
- Separated implementation status from architectural documentation

## [2025-10-28] - 0.2.0 - LLM -> JSON Plan -> SQL

### Added
- Query builder module capable of turning simple structured JSON into SQL
    - Support simple selects, spatial filters, spatial joins, attribute joins
    - Does not support groups, aggregates, or other SQL components
- Vector embedding database for RAG
    - DB schemas stored as embeddings to better match relevant tables in prompt creation
    - User query examples + JSON plans stored as embeddings to use only relevant examples in few-shot cache

### Changed
- LLM now generates JSON plan instead of raw SQL for more consistent query creation
- Examples and table schemas are now matched via vector embedding to use query to better show only relevant examples to the LLM

## [2025-09-24] - 0.1.0 - First Live Demo

### Changed
- First [live demo](https://geoff.connorcrowe.ca) of Geoff available 