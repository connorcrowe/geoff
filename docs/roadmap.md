# Roadmap
**Purpose: To outline the priority and functionality of future features**

## Prioritized Features
### 1. Layer History
Show the previous queries results in a "layers" panel on the frontend. Allow simple interaction like toggling visibility, deleting, etc. Use LLM inferred name, allow user rename.

### 2. Synthetic Geometry ("Create")
Geoff currently can only accept DB results to turn into layers with geometry. Add a module that allows for the creation of new geometries
- Relative to existing geometries:
    - Buffer
    - Centroid
- Eventually:
    - Route / path creation

### 3. Previous Layer References
Allow the user to explicitly reference previous layer results as an input for a next question. 
- Ex: 
    - Q1: Show all schools -> A1: Returns geometry layer of schools
    - Q2: Show a 100m buffer around @schools layer -> A2: Returns buffer

## Unprioritized
### Model Transparency & Explanation
Show helpful information to the user about successful and unsuccessful queries
- Show SQL or components to help understand which DB tables and SQL components are being used/attempted
- Explain common error cases to the user (no results found, that data isn't available, etc.)
- Short summary from the LLM explaining its thinking
- (Stretch) LLM asks follow up questions before creating the JSON

This opens the door to several powerful features:
- Once a result is generated, show the SQL as structured input fields and allow the user to tweak them
    - E.g. Change "500m buffer" to "300m buffer" with a slider and see results change without new LLM call.
- Specific user-correction
    - The user can identify a flaw in output or logic and inject specific correction via prompt.

### "Route"
User can request a path between two places with some criteria to prioritize.
- Show the shortest path between Liberty Village and the Annex that passes through the most parks on foot.

### Place Resolution
System by which ambiguous place names are resolved. A user can specify any of the below and the application is able to reason about what they are referring to and how that place contains/overlaps/relates to other places
- This address
- University of Toronto campus
- "University" neighbourhood
- "University-Rosedale" ward