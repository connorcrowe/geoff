# config/examples.py
"""Contains example PostGIS syntax for common queries for each table"""

# Format
    # {
    #     "tables": [""],
    #     "user_query": "",
    #     "sql":"""
    #         SELECT ;
    #     """
    # },

examples = [
    # --- AMBULANCE_STATIONS
    {
        "tables": ["ambulance_stations"],
        "user_query": "Where are the ambulance stations?",
        "sql":"""
            SELECT geometry, name, address, municipality FROM ambulance_stations;
        """
    },
    {
        "tables": ["ambulance_stations"],
        "user_query": "Show me ems stations in Scarborough",
        "sql":"""
            SELECT geometry, name, address FROM ambulance_stations
            WHERE municipality ILIKE '%Scarborough%';
        """
    },

    # --- BIKE_LANES
    {
        "tables": ["bike_lanes"],
        "user_query": "Show bike lanes installed after 2020",
        "sql":"""
            SELECT * FROM bike_lanes WHERE installed_year >= 2020;
        """
    },
    {
        "tables": ["bike_lanes"],
        "user_query": "Show all bike lanes and when they were installed",
        "sql":"""
            SELECT geometry, street_name, install_year FROM bike_lanes ORDER BY installed_year DESC;
        """
    },
    {
        "tables": ["bike_lanes"],
        "user_query": "Give me all the bike lanes that are not sharrows",
        "sql":"""
            SELECT geometry, street_name, lane_type, install_year FROM bike_lanes 
            WHERE lane_type NOT ILIKE lower('%sharrow%');
        """
    },
    {
        "tables": ["bike_lanes"],
        "user_query": "Show me the protected bike lanes in Toronto",
        "sql":"""
            SELECT geometry, street_name, lane_type, install_year FROM bike_lanes 
            WHERE lane_type NOT ILIKE '%sharrow%' AND lane_type NOT ILIKE '%signed route%';
        """
    },
    {
        "tables": ["bike_lanes"],
        "user_query": "Show me all the contraflow bike lanes",
        "sql":"""
            SELECT geometry, street_name, lane_type, install_year FROM bike_lanes 
            WHERE lane_type ILIKE '%contraflow%';
        """
    },
    
    # --- FIRE_STATIONS
    {
        "tables": ["fire_stations"],
        "user_query": "Show all the fire stations",
        "sql":"""
            SELECT geometry, address, municipality, year_built FROM fire_stations;
        """
    },
    {
        "tables": ["fire_stations"],
        "user_query": "Show me fire stations in North York",
        "sql":"""
            SELECT geometry, address, year_built FROM fire_stations
            WHERE municipality ILIKE '%North York%';
        """
    },
    {
        "tables": ["fire_stations"],
        "user_query": "Show me fire stations built after 1990",
        "sql":"""
            SELECT geometry, address, year_built FROM fire_stations
            WHERE year_built > 1990;
        """
    },

    # --- NEIGHBOURHOODS
    {
        "tables": ["neighbourhoods"],
        "user_query": "Show the neighbourhoods of Toronto",
        "sql":"""
            SELECT geometry, area_name FROM neighbourhoods;
        """
    },
    {
        "tables": ["neighbourhoods"],
        "user_query": "Which neighbourhoods are classified as improvement areas?",
        "sql":"""
            SELECT geometry, area_name, classification FROM neighbourhoods
            WHERE classification_code ILIKE '%NIA%';
        """
    },
    {
        "tables": ["neighbourhoods"],
        "user_query": "Which neighbourhoods are classified as emerging neighbourhoods?",
        "sql":"""
            SELECT geometry, area_name, classification FROM neighbourhoods
            WHERE classification_code ILIKE '%EN%';
        """
    },
        {
        "tables": ["neighbourhoods"],
        "user_query": "Which neighbourhoods are the biggest?",
        "sql":"""
            SELECT geometry, area_name, ROUND(ST_Area(geometry::geography)) AS area_sq_m FROM neighbourhoods
            ORDER BY area_sq_m DESC LIMIT 10;
        """
    },

    # --- PARKS
    {
        "tables": ["parks"],
        "user_query": "Show the parks in Toronto",
        "sql":"""
            SELECT geometry, name, type FROM parks;
        """
    },
    {
        "tables": ["parks"],
        "user_query": "Show the community centres in Toronto",
        "sql":"""
            SELECT geometry, name FROM parks WHERE type = "Community Centre";
        """
    },
    {
        "tables": ["parks"],
        "user_query": "Show the dog parks in Toronto",
        "sql":"""
            SELECT geometry, name, amenities FROM parks WHERE amenities ILIKE '%dog%';
        """
    },
    {
        "tables": ["parks"],
        "user_query": "Show parks with playgrounds",
        "sql":"""
            SELECT geometry, name, amenities FROM parks WHERE amenities ILIKE '%playground%;
        """
    },
    {
        "tables": ["parks"],
        "user_query": "Which parks are bigger than 100 square meters?",
        "sql":"""
            SELECT geometry, name, ROUND(ST_Area(geometry::geography)) AS area_sq_m FROM parks 
            WHERE area_sq_m > 100 ORDER BY area_sq_m DESC;
        """
    },

    # --- POLICE_STATIONS
    {
        "tables": ["police_stations"],
        "user_query": "Show me police stations",
        "sql":"""
            SELECT geometry, name, address FROM police_stations;
        """
    },

    # --- SCHOOLS
    {
        "tables": ["schools"],
        "user_query": "Show me schools",
        "sql":"""
            SELECT geometry, name, address, school_board_name, school_type_desc FROM schools;
        """
    },
    {
        "tables": ["schools"],
        "user_query": "Where are the french schools?",
        "sql":"""
            SELECT geometry, name, address, school_board_name, school_type_desc FROM schools
            WHERE school_type_desc ILIKE '%French%';
        """
    },
    {
        "tables": ["schools"],
        "user_query": "How many public schools are there?",
        "sql":"""
            SELECT geometry, name, address, school_board_name, school_type_desc FROM schools
            WHERE school_type_desc ILIKE '%Public%';
        """
    },
    {
        "tables": ["schools"],
        "user_query": "Show me private schools",
        "sql":"""
            SELECT geometry, name, address, school_board_name, school_type_desc FROM schools
            WHERE school_type_desc ILIKE '%Private%';
        """
    },
    {
        "tables": ["schools"],
        "user_query": "Which schools are in the Toronto District School Board?",
        "sql":"""
            SELECT geometry, name, address, school_type_desc FROM schools
            WHERE school_board_name ILIKE '%Toronto District School Board%';
        """
    },
    
    # --- Single table: Streets
    # {
    #     "tables": ["streets"],
    #     "user_query": "Show the streets of Toronto",
    #     "sql":"""
    #         SELECT geometry, name, type FROM streets;
    #     """
    # },

]