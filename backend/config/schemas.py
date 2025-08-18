schemas = {
    "bike_lanes": """
    CREATE TABLE bike_lanes (
        id SERIAL PRIMARY KEY,
        installed_year INT,         -- year the bike lane was first installed
        upgraded_year INT,          -- year the bike lane was last upgraded
        street_name TEXT,           -- primary street name where the bike lane is located
        from_street TEXT,           -- cross street marking the start of the lane
        to_street TEXT,             -- cross street marking the end of the lane
        lane_type TEXT,       -- the type of infrastructure (e.g. sharrows, bike lane, multi-use trail, etc.)
        geometry GEOMETRY(LineString, 4326) -- spatial geometry of the bike lane
    );
    """,

    "neighbourhoods": """
    CREATE TABLE neighbourhoods (
        id SERIAL PRIMARY KEY,
        area_name TEXT,             -- official neighbourhood name
        area_desc TEXT,              -- descriptive text about the neighbourhood
        classification TEXT,         -- classification for improvement or zoning type
        geometry GEOMETRY(Polygon, 4326) -- boundary polygon for the neighbourhood
    );
    """,

    "parks": """
    CREATE TABLE parks (
        id SERIAL PRIMARY KEY,
        name TEXT,                   -- official park name
        type TEXT,                   -- category of park 
        amenities TEXT,              -- amenities in the park
        geometry GEOMETRY(Polygon, 4326) -- boundary polygon for the park
    );
    """
}

schema_descriptions = {
    "bike_lanes": "Bike lane segments in Toronto with installation and upgrade years, location street names, and geospatial geometry.",
    "neighbourhoods": "Toronto neighbourhood boundaries with descriptions and improvement classification.",
    "parks": "Toronto parks including type, amenities, and location boundaries."
}
