# Geoff: Natural language interface for exploring spatial data
###### *Connor Crowe*
GEOFF (GEOspatial Fact Finder) takes prompts in natural language, converts them into spatial SQL queries, and displays results on a map - shortening the time from question to insight for planners, geographers, and more.

## Problem Statement
**Motivation**
*Many questions can be answered with a map.* Questions from urban mobility to planning to climate response and more can be answered with geospatial data, but can require complex spatial SQL queries and data cleaning that is non-trivial for non-technical users.

Geoff is an experiment in making answers more accessible by turning plain English into spatial queries and mapping the results.

**Problem**
Planners, NGOs, activists, public employees have questions with geospatial answers but are often limited by the collection and querying of spatial data.

## Current
### State of Development
Preliminary datasets have been cleaned and prepped for testing. DB is quickly set up in a docker container. Current models are (for now) hosted locally on my homelab and accessed via Ollama. A python script takes a user prompt to the model with a custom system prompt that outlines the DB schema and returns a spatial SQL query.

**Status**: Great to have data flowing through the pipes. Model performance is still wildly inconsistent.

### Capabilities
**Currently Integrated Data**
- Bike lanes in Toronto (type of lane, year installed)
- Neighbourhoods in Toronto
- *More coming soon*

**Current Ability**
- Manual spatial queries on data (cleaned and joined)
- Mid-accuracy spatial SQL generated from English prompt
    - Models in experimentation: mistral, mixtral, sqlcoder, llama3.2
- Model improvements so far:
    - System prompting

### Architecture
1. User enters a natural language question
2. Python backend prompts a local LLM (Mistral, SQLCoder)
3. LLM generates a PostGIS query against a local database
4. Query is run and results are visualized on a web map

**Tech Stack**
- Python
- PostGIS & PostgreSQL
- Ollama (local LLMs)
- Leaflet.js
- FastAPI
- Docker

### Limits
- Model is inconsistent
- Does not validate SQL before attempting execution
- No UI / map
- Model doesn't fully understand spatial functions
- Model occasionally adds requirements not asked for

## Future
**Future Data**
- All streets and sidewalks (OSM)
- Transit stops
- Zoning
- Trees
- Water
- Population density
- Demographics

**Future Ability**
- Model improvements:
    - Further system prompting
    - Experimentation with other models
        - Including further SQL tuned models
    - Custom fine-tuning on spatial SQL
    - Post-processing
        - Automatic syntax validation
        - Schema-aware validation
    - Stretch: Few-shot cache
    - Stretch: Retrieval layer
    - Stretch: Learning from user feedback/flags
- Visualization
    - Display results on leaflet web map
    - 
    - Stretch: explore results via map (hover, clickthrough, etc.)
