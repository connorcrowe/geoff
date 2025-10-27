# config/examples.py
"""Contains example PostGIS syntax for common queries for each table"""

examples = [
    # --- WARDS
    {
        "tables": ["wards"],
        "user_query": "Show all wards",
        "sql": """SELECT geometry, name, ward_id FROM wards;
        """
    },
    # --- AMBULANCE_STATIONS
    {
        "tables": ["ambulance_stations"],
        "user_query": "Show all ambulance stations",
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

    # --- ATTRACTIONS
    {
        "tables": ["attractions"],
        "user_query": "Show all attractions, their type, their address, their website, and their descriptions",
        "sql": """
            SELECT geometry, name, category, address, description, website
            FROM attractions;
        """
    },
    {
        "tables": ["attractions"],
        "user_query": "Show all museums in the city",
        "sql": """
            SELECT geometry, name, address, description FROM attractions
            WHERE category = 'Museum';
        """
    },
    {
        "tables": ["attractions"],
        "user_query": "List all performing arts venues",
        "sql": """
            SELECT geometry, name, address, description FROM attractions
            WHERE category = 'Performing Arts';
        """
    },
    {
        "tables": ["attractions"],
        "user_query": "Which ward has the most attractions?",
        "sql": """
            SELECT ward, COUNT(*) AS num_attractions
            FROM attractions
            GROUP BY ward
            ORDER BY num_attractions DESC
            LIMIT 1;
        """
    },
    {
        "tables": ["attractions"],
        "user_query": "Show all visitor information points",
        "sql": """
            SELECT geometry, name, address, municipality FROM attractions
            WHERE category = 'Visitor Information';
        """
    },
    {
        "tables": ["attractions"],
        "user_query": "Where is the attraction Medieval Times?",
        "sql": """
            SELECT geometry, name, address, description FROM attractions
            WHERE name ILIKE '%Medieval Times%';
        """
    },

    # --- BIKE_LANES
    {
        "tables": ["bike_lanes"],
        "user_query": "Show all bike lanes, their type, and when they were installed",
        "sql":"""
            SELECT geometry, street_name, install_year FROM bike_lanes ORDER BY installed_year DESC;
        """
    },
    {
        "tables": ["bike_lanes"],
        "user_query": "Show bike lanes installed after 2020",
        "sql":"""
            SELECT * FROM bike_lanes WHERE installed_year >= 2020;
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
    {
        "tables": ["bike_lanes"],
        "user_query": "Show all bike lanes installed after 2020 within 500m of schools",
        "sql":"""
            SELECT geometry, street_name, lane_type, install_year, COUNT(s.id) AS schools_within_500m
            FROM bike_lanes bl
            JOIN schools s ON ST_DWithin(bl.geometry::geography, s.geometry::geography, 500)
            WHERE bl.installed_year IS NOT NULL AND bl.installed_year >= 2020 GROUP BY bl.geometry, bl.street_name, bl.lane_type, bl.installed_year;
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
        "user_query": "Show all the neighbourhoods",
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
    # --- PARKING LOTS
    {
        "tables": ["parking_lots"],
        "user_query": "Show every parking lot",
        "sql":"""
            SELECT geometry, id, last_updated FROM parking_lots;
        """
    },
    {
        "tables": ["parking_lots"],
        "user_query": "Which parking lots are the biggest?",
        "sql":"""
            SELECT id, geometry, ST_Area(geometry::geography) AS area_m2, last_updated FROM parking_lots ORDER BY area_m2 DESC;
        """
    },
    {
        "tables": ["parking_lots"],
        "user_query": "Which parking lot is the biggest?",
        "sql":"""
            SELECT id, geometry, ST_Area(geometry::geography) AS area_m2 FROM parking_lots ORDER BY area_m2 DESC LIMIT 1;
        """
    },
    {
        "tables": ["parking_lots"],
        "user_query": "What is the total area covered by parking lots?",
        "sql":"""
            SELECT ST_Union(geometry) AS all_parking_lots_geom, SUM(ST_Area(geometry::geography)) AS total_area_m2 FROM parking_lots;
        """
    },

    # --- PARKS
    {
        "tables": ["parks"],
        "user_query": "Show every park",
        "sql":"""
            SELECT geometry, name, type, amenities FROM parks;
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
        "user_query": "Where are dog parks located?",
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

    # --- POLICE_STATIONS
    {
        "tables": ["police_stations"],
        "user_query": "Show all police stations",
        "sql":"""
            SELECT geometry, name, address FROM police_stations;
        """
    },

    # --- SCHOOLS
    {
        "tables": ["schools"],
        "user_query": "Show all schools",
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

examples_json = [

    #✓ --- select/1.0                --- Single table 
    {
        "user_query": "Show all schools",
        "plan": {
            "action": "select",
            "groups": [
                {"source_tables": [
                    {"table": "schools", "columns": ["name", "school_type_desc"], "filters": []}
                ]}
            ]
        }
    },
        #✓ --- select/1.0                --- Single table, filter (str)
    {
        "user_query": "Show all neighbourhoods with classification 'Emerging'",
        "plan": {
            "action": "select",
            "groups": [
                {"source_tables": [
                    {
                        "table": "neighbourhoods",
                        "columns": ["area_name", "classification", "geometry"],
                        "filters": [{"column": "classification_code", "operator": "ILIKE", "value": "%EN%"}]
                    }
                ]}
            ]
        }
    },
        #✓ --- select/1.0                --- Single table, filter (num)
    {
        "user_query": "Get all fire stations built before 1980",
        "plan": {
            "action": "select",
            "groups": [
                {"source_tables": [
                    {
                        "table": "fire_stations",
                        "columns": ["station_no", "address", "year_built", "geometry"],
                        "filters": [{"column": "year_built", "operator": "<", "value": 1980}]
                    }
                ]}
            ]
            
        }
    },

    #✓ --- select/2.0                --- Multi table, unrelated, separate
    {
        "user_query": "Show schools and parks together",
        "plan": {
            "action": "select",
            "groups": [
                {"source_tables": [
                    {
                        "table": "schools",
                        "columns": ["name", "school_type_desc", "geometry"],
                        "filters": []
                    }
                ]},
                {"source_tables": [
                    {
                        "table": "parks",
                        "columns": ["name", "type", "geometry"],
                        "filters": []
                    }
                ]}
            ]
        }
    },

    #✓ --- select/2.1.1-distance     --- Spatial filter, exists, dwithin
    {
        "user_query": "Show all bike lanes within 500 meters of schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": ["street_name", "lane_type", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "schools",
                            "columns": ["name", "school_type_desc", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "exists",
                            "left_table": "bike_lanes",
                            "right_table": "schools",
                            "params": {"distance_meters": 500},
                        }
                    ]
                }
            ]
        }
    },
    {
        "user_query": "Show all bike lanes within 500 meters of private schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": ["street_name", "lane_type", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "schools",
                            "columns": ["name", "school_type_desc", "geometry"],
                            "filters": [{"column": "school_type_desc", "operator": "ILIKE", "value": "%private%"}]
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "exists",
                            "left_table": "bike_lanes",
                            "right_table": "schools",
                            "params": {"distance_meters": 500},
                        }
                    ]
                }
            ]
        }
    },

    #✓ --- select/2.1.1-intersects   --- Spatial filter, exists, intersects
    {
        "user_query": "Show all neighbourhoods that intersect ward boundaries",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "neighbourhoods",
                            "columns": ["area_name", "classification", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "wards",
                            "columns": ["name", "ward_id", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_intersects",
                            "clause": "exists",
                            "left_table": "neighbourhoods",
                            "right_table": "wards"
                        }
                    ]
                }
            ]
        }
    },

    #✓ --- select/2.1.2-distance     --- Spatial join, join, dwithin
    {
        "user_query": "List each school and the nearest fire station within 1 kilometer",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": ["name", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "fire_stations",
                            "columns": ["station_no", "address", "municipality", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "join",
                            "left_table": "schools",
                            "right_table": "fire_stations",
                            "params": {"distance_meters": 1000}
                        }
                    ]
                }
            ]
        }
    },

    #✓ --- select/2.1.2-intersects   --- Spatial join, join, intersects
    {
        "user_query": "List all parks and the neighbourhoods they fall within",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": ["name", "type", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "neighbourhoods",
                            "columns": ["area_name", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_intersects",
                            "clause": "join",
                            "left_table": "parks",
                            "right_table": "neighbourhoods"
                        }
                    ]
                }
            ]
        }
    },

    #X(I) --- select/2.1.3-dwithin      --- Spatial join, left join, dwithin
    {
        "user_query": "Show all ambulance stations and any attractions within 250 meters, if available",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "ambulance_stations",
                            "columns": ["name", "municipality", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "attractions",
                            "columns": ["name", "category", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "left join",
                            "left_table": "ambulance_stations",
                            "right_table": "attractions",
                            "params": {"distance_meters": 250}
                        }
                    ]
                }
            ]
        }
    },

    #X(I) --- select/2.1.3-intersects   --- Spatial join, left join, intersects
    {
        "user_query": "Show all bike lanes and the ward they pass through, even if some aren't inside any ward",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": ["street_name", "lane_type", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "wards",
                            "columns": ["name", "ward_id", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_intersects",
                            "clause": "left join",
                            "left_table": "bike_lanes",
                            "right_table": "wards"
                        }
                    ]
                }
            ]
        }
    },

    #✓ --- select/2.2.1              --- Attribute filter, exists
    {
        "user_query": "Show the ward that the Allan Gardens are in",
        "plan": {
            "action": "select",
            "groups": [
            {
                "source_tables": [
                    {"table": "wards", "columns": ["name", "ward_id", "geometry"], "filters": []},
                    {"table": "attractions", "columns": ["name", "category", "address", "ward_id", "geometry"], "filters": [{"column": "name", "operator": "ILIKE", "value": "Allan Gardens"}]}
                ],
                "relations": [
                {
                    "type": "attribute",
                    "method": "=",
                    "clause": "exists",
                    "left_table": "wards",
                    "right_table": "attractions",
                    "params":{"left_column": "ward_id", "right_column": "ward_id"}
                }
                ]
            }
            ]
        }
    },

    #✓ --- select/2.2.2              --- Attribute join, join      (Note: this one points out a frontend ambiguous column name issue)
    {
        "user_query": "Join attractions with wards by matching ward_id",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": ["name", "ward_id", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "wards",
                            "columns": ["ward_id", "name", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "attribute",
                            "method": "=",
                            "clause": "join",
                            "left_table": "attractions",
                            "right_table": "wards",
                            "params": {"left_column": "ward_id", "right_column": "ward_id"}
                            
                        }
                    ]
                }
            ]
        }
    },

    #X(I) --- select/2.2.3              --- Atribute join, left join
    {
        "user_query": "List all wards and any attractions that belong to them, even if some wards have none",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "wards",
                            "columns": ["name", "ward_id", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "attractions",
                            "columns": ["name", "ward_id", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "attribute",
                            "method": "=",
                            "clause": "left join",
                            "left_table": "wards",
                            "left_column": "ward_id",
                            "right_table": "attractions",
                            "right_column": "ward_id"
                        }
                    ]
                }
            ]
        }
    }


    # NOT IMPLEMENTED - 2.2 (Layers: 2) Multi layer, filtered (spatial, exists, st_contains)
    # {
    #     "user_query": "Show neighbourhoods that contain at least one fire station",
    #     "plan": {
    #         "action": "select",
    #         "groups": [
    #         {
    #             "source_tables": [
    #                 {"table": "neighbourhoods", "columns": ["area_name", "geometry"], "filters": []},
    #                 {"table": "fire_stations", "columns": ["id", "geometry"], "filters": []}
    #             ],
    #             "relations": [
    #             {
    #                 "type": "spatial",
    #                 "method": "st_contains",
    #                 "clause": "exists",
    #                 "left_table": "neighbourhoods",
    #                 "right_table": "fire_stations",
    #                 "params": {}
    #             }
    #             ]
    #         }
    #         ]
    #     }
    # },

    # BROKEN (AMBIGUOUS) - 2.3 (Layers: 2) Multi layer, joined (spatial, join, st_dwithin)
    # {
    #     "user_query": "List all schools and nearby fire stations within 300 meters",
    #     "plan": {
    #         "action": "select",
    #         "groups": [
    #         {
    #             "source_tables": [
    #                 {"table": "schools", "columns": ["name", "school_type_desc", "geometry"], "filters": []},
    #                 {"table": "fire_stations", "columns": ["address", "municipality"], "filters": []}
    #             ],
    #             "relations": [
    #             {
    #                 "type": "spatial",
    #                 "method": "st_dwithin",
    #                 "clause": "join",
    #                 "left_table": "schools",
    #                 "right_table": "fire_stations",
    #                 "params": {"distance_meters": 300}
    #             }
    #             ]
    #         }
    #         ]
    #     }
    # },

    # # BROKEN (AMBIGUOUS) - 2.3 (Layers: 2) Multi layer, joined (spatial, join, st_contains)
    # {
    #     "user_query": "Find which neighbourhood each park is located in",
    #     "plan": {
    #         "action": "select",
    #         "groups": [
    #         {
    #             "source_tables": [
    #                 {"table": "parks", "columns": ["name", "type", "geometry"], "filters": []},
    #                 {"table": "neighbourhoods", "columns": ["area_name", "geometry"], "filters": []}
    #             ],
    #             "relations": [
    #             {
    #                 "type": "spatial",
    #                 "method": "st_contains",
    #                 "clause": "join",
    #                 "left_table": "neighbourhoods",
    #                 "right_table": "parks",
    #                 "params": {}
    #             }
    #             ]
    #         }
    #         ]
    #     }
    # },

    # 2.4 Multi layer, joined (attribute, join)
    # {
    #     "user_query": "Show the attractions in each ward",
    #     "plan": {
    #         "action": "select",
    #         "groups": [
    #         {
    #             "source_tables": [
    #                 {"table": "wards", "columns": ["name", "ward_id", "geometry"], "filters": []},
    #                 {"table": "attractions", "columns": ["name", "category", "address", "ward_id", "geometry"], "filters": []}
    #             ],
    #             "relations": [
    #             {
    #                 "type": "attribute",
                    
    #                 "clause": "join",
    #                 "left_table": "wards",
    #                 "right_table": "attractions",
    #                 "on":{"left_column": "ward_id", "right_column": "ward_id"}
    #             }
    #             ]
    #         }
    #         ]
    #     }
    # },


]