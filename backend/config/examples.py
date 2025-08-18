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
    # --- Single table: `bike_lanes` ---
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

]