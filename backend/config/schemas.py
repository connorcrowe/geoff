import re

schemas = {
    "ambulance_stations": """
    CREATE TABLE ambulance_stations (
        id SERIAL PRIMARY KEY,
        address TEXT,               -- street address
        municipality TEXT,          -- municipality
        name TEXT,                  -- name
        ems_id INT,                 -- ems id number
        ems_name TEXT,              -- name of stations
        ems_website TEXT,           -- website
        geometry GEOMETRY(Point, 4326) -- geometry location of the station
    );
    """,
    
    "bike_lanes": """
    CREATE TABLE bike_lanes (
        id SERIAL PRIMARY KEY,
        installed_year INT,         -- year the bike lane was first installed
        upgraded_year INT,          -- year the bike lane was last upgraded
        street_name TEXT,           -- primary street name where the bike lane is located
        from_street TEXT,           -- cross street marking the start of the lane
        to_street TEXT,             -- cross street marking the end of the lane
        lane_type TEXT,             -- the type of infrastructure (e.g. sharrows, bike lane, multi-use trail, etc.)
        converted TEXT,             -- year the bike lane was converted
        geometry GEOMETRY(LineString, 4326) -- spatial geometry of the bike lane
    );
    """,

    "fire_stations": """
    CREATE TABLE fire_stations (
        id SERIAL PRIMARY KEY,
        address TEXT,               -- street address of fire stations
        municipality TEXT,          -- municipality of station
        station_no TEXT,            -- number of station
        year_built INT,             -- year station built
        type TEXT,                  -- Fire Station or Operaitons centre
        geometry GEOMETRY(Point, 4326) -- geometry location of the station
    );
    """,

    "neighbourhoods": """
    CREATE TABLE neighbourhoods (
        id SERIAL PRIMARY KEY,
        area_name TEXT,             -- official neighbourhood name
        classification_code TEXT,   -- classification tag for improvement or emerging type
        classification TEXT,        -- classification title for improvement or emerging type
        geometry GEOMETRY(Polygon, 4326) -- boundary polygon for the neighbourhood
    );
    """,

    "parking_lots": """
    CREATE TABLE parking_lots (
        id SERIAL PRIMARY KEY,
        last_updated TEXT,          -- Date of last change to geometry or attribute data
        geometry GEOMETRY(Polygon, 4326) -- Boundary polygon of the parking lot
    );
    """,

    "parks": """
    CREATE TABLE parks (
        id SERIAL PRIMARY KEY,
        name TEXT,                   -- official park name
        type TEXT,                   -- category of park 
        amenities TEXT,              -- list of amenities in the park
        geometry GEOMETRY(Point, 4326) -- point location for the park
    );
    """,

    "police_stations": """
    CREATE TABLE police_stations (
        id SERIAL PRIMARY KEY,
        name TEXT,               -- name of station
        address TEXT,                -- street address
        geometry GEOMETRY(Point, 4326) -- geometry location of the station
    );
    """,

    "schools": """
    CREATE TABLE schools (
        id SERIAL PRIMARY KEY,
        name TEXT,                   -- name of the school
        school_type TEXT,            -- short code for type (FP - French Public, FS - French Separate, EP - English Public, ES - English Separate, PR - Private)
        school_type_desc TEXT,       -- long form of type
        school_board_name TEXT,      -- school board name
        address TEXT,                -- street address
        geometry GEOMETRY(Point, 4326) -- geometry location of the station
    );
    """

    # "streets": """
    # CREATE TABLE streets (
    #     id SERIAL PRIMARY KEY,
    #     name TEXT,                   -- official street name
    #     type TEXT,                   -- category of roadway (OSM 'highway' type)
    #     geometry GEOMETRY(LineString, 4326) -- geometry of the street
    # );
    # """
}

schema_descriptions = {
    "bike_lanes": "Bike lane segments in Toronto with installation and upgrade years, location street names, and geospatial geometry.",
    "neighbourhoods": "Toronto neighbourhood boundaries with descriptions and improvement classification.",
    "parks": "Toronto parks including type, amenities, and location boundaries.",
    "streets": "All roads and streets in Toronto, with their associated OpenStreetMap 'highway' type."
}

# Convert schemas to JSON format for frontend data dicts
def parse_schema(sql: str):
    columns = []
    for line in sql.splitlines():
        line = line.strip()
        if not line or line.upper().startswith("CREATE TABLE") or line.startswith(");"):
            continue
        parts = line.split("--")
        column_part = parts[0].strip().rstrip(",")
        comment = parts[1].strip() if len(parts) > 1 else ""
        match = re.match(r"(\w+)\s+(.+)", column_part)
        if match:
            name, col_type = match.groups()
            columns.append({"name": name, "type": col_type, "description": comment})
    return columns

def get_parsed_schemas():
    return {table: parse_schema(sql) for table, sql in schemas.items()}