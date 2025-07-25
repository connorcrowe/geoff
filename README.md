# Geoff
Geoff (GEOspatial Fact Finder) turns natural language into spatial queries and shows results on a map.

## Summary
Many questions can be answered with geospatial data. "How many schools are near bike lanes?" But gathering and querying this data requires specialized skill. 

**Geoff is an AI agent that helps turn questions into geospatial answers"**

## Completed Development:
- Created dockerized database with PostGIS
- Imported datasets with spatial data:
    - Bike Lanes
    - Neighbourhoods

## Current Milestone:
- Create simple LLM script to produce spatial SQL queries
- Manually validate those queries

## Future Milestones:
- Display the SQL result on a web map
- Expand datasets

## Appendix: Repo Structure
```
geoff/
├── backend/
├── frontend/
├── db/
```