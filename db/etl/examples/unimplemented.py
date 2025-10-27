examples_pending_implementation = [
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
]

example_format = [
    # Spatial
    {
        "type": "select_2.1.1-distance",
        "sources": ["x", "y"],
        
        "user_query": "question",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "x",
                            "columns": ["a", "b", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "y",
                            "columns": ["a", "b", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "exists",
                            "left_table": "x",
                            "right_table": "y",
                            "params": {"distance_meters": 500},
                        }
                    ]
                }
            ]
        }
    },

    # Attribute
    {
        "type": "select_2.2.2",
        "sources": ["x", "y"],
        
        "user_query": "question",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "x",
                            "columns": ["name", "key", "geometry"],
                            "filters": []
                        },
                        {
                            "table": "y",
                            "columns": ["key", "name", "geometry"],
                            "filters": []
                        }
                    ],
                    "relations": [
                        {
                            "type": "attribute",
                            "method": "=",
                            "clause": "join",
                            "left_table": "x",
                            "right_table": "y",
                            "params": {"left_column": "key", "right_column": "key"}
                            
                        }
                    ]
                }
            ]
        }
    },
]