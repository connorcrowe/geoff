examples_embedded = [
    {
        "type": "select_1.0",
        "sources": [
            "fire_stations"
        ],
        "user_query": "Get all fire stations built before 1980",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "fire_stations",
                            "columns": [
                                "station_no",
                                "address",
                                "year_built",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "year_built",
                                    "operator": "<",
                                    "value": 1980
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.0",
        "sources": [
            "schools",
            "parks"
        ],
        "user_query": "Show schools and parks together",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "school_type_desc",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                },
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": [
                                "name",
                                "type",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.1.1-distance",
        "sources": [
            "bike_lanes",
            "schools"
        ],
        "user_query": "Show all bike lanes within 500 meters of schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": [
                                "street_name",
                                "lane_type",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "school_type_desc",
                                "geometry"
                            ],
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
                            "params": {
                                "distance_meters": 500
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.1.1-distance",
        "sources": [
            "bike_lanes",
            "schools"
        ],
        "user_query": "Show all bike lanes within 500 meters of private schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": [
                                "street_name",
                                "lane_type",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "school_type_desc",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "school_type_desc",
                                    "operator": "ILIKE",
                                    "value": "%private%"
                                }
                            ]
                        }
                    ],
                    "relations": [
                        {
                            "type": "spatial",
                            "method": "st_dwithin",
                            "clause": "exists",
                            "left_table": "bike_lanes",
                            "right_table": "schools",
                            "params": {
                                "distance_meters": 500
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.1.1-intersects",
        "sources": [
            "neighbourhoods",
            "wards"
        ],
        "user_query": "Show all neighbourhoods that intersect ward boundaries",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "neighbourhoods",
                            "columns": [
                                "area_name",
                                "classification",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "wards",
                            "columns": [
                                "name",
                                "ward_id",
                                "geometry"
                            ],
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
    {
        "type": "select_2.1.2-distance",
        "sources": [
            "schools",
            "fire_stations"
        ],
        "user_query": "List each school and the nearest fire station within 1 kilometer",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "fire_stations",
                            "columns": [
                                "station_no",
                                "address",
                                "municipality",
                                "geometry"
                            ],
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
                            "params": {
                                "distance_meters": 1000
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.1.2-intersects",
        "sources": [
            "parks",
            "neighbourhoods"
        ],
        "user_query": "List all parks and the neighbourhoods they fall within",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": [
                                "name",
                                "type",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "neighbourhoods",
                            "columns": [
                                "area_name",
                                "geometry"
                            ],
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
    {
        "type": "select_2.2.1",
        "sources": [
            "wards",
            "attractions"
        ],
        "user_query": "Show the ward that the Allan Gardens are in",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "wards",
                            "columns": [
                                "name",
                                "ward_id",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "category",
                                "address",
                                "ward_id",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "name",
                                    "operator": "ILIKE",
                                    "value": "Allan Gardens"
                                }
                            ]
                        }
                    ],
                    "relations": [
                        {
                            "type": "attribute",
                            "method": "=",
                            "clause": "exists",
                            "left_table": "wards",
                            "right_table": "attractions",
                            "params": {
                                "left_column": "ward_id",
                                "right_column": "ward_id"
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_2.2.2",
        "sources": [
            "attractions",
            "wards"
        ],
        "user_query": "Join attractions with wards by matching ward_id",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "ward_id",
                                "geometry"
                            ],
                            "filters": []
                        },
                        {
                            "table": "wards",
                            "columns": [
                                "ward_id",
                                "name",
                                "geometry"
                            ],
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
                            "params": {
                                "left_column": "ward_id",
                                "right_column": "ward_id"
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "ambulance_stations"
        ],
        "user_query": "Show all ambulance stations",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "ambulance_stations",
                            "columns": [
                                "name",
                                "ems_name",
                                "address",
                                "municipality",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "bike_lanes"
        ],
        "user_query": "Show all bike lanes",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": [
                                "street_name",
                                "lane_type",
                                "installed_year",
                                "upgraded_year",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "fire_stations"
        ],
        "user_query": "Show all fire stations",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "fire_stations",
                            "columns": [
                                "address",
                                "station_no",
                                "type",
                                "year_built",
                                "municipality",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "neighbourhoods"
        ],
        "user_query": "Show all neighbourhoods",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "neighbourhoods",
                            "columns": [
                                "area_name",
                                "classification",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "parking_lots"
        ],
        "user_query": "Show all parking lots",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parking_lots",
                            "columns": [
                                "id",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "parks"
        ],
        "user_query": "Show all parks",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": [
                                "name",
                                "type",
                                "amenities",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "police_stations"
        ],
        "user_query": "Show all police stations",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "police_stations",
                            "columns": [
                                "name",
                                "address",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "schools"
        ],
        "user_query": "Show all schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "address",
                                "school_board_name",
                                "school_type_desc",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "wards"
        ],
        "user_query": "Show all wards",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "wards",
                            "columns": [
                                "name",
                                "ward_id",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "attractions"
        ],
        "user_query": "Show all attractions",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "category",
                                "address",
                                "description",
                                "geometry"
                            ],
                            "filters": []
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "attractions"
        ],
        "user_query": "Show all museums",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "category",
                                "address",
                                "description",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "category",
                                    "operator": "ILIKE",
                                    "value": "%museum%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "bike_lanes"
        ],
        "user_query": "Show all bike lanes that are not sharrows",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": [
                                "street_name",
                                "type",
                                "installed_year",
                                "upgraded_year",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "category",
                                    "operator": "NOT ILIKE",
                                    "value": "%sharrow%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "schools"
        ],
        "user_query": "Which schools are in the Toronto District School Board?",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "school_board_name",
                                "school_type",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "value": "Toronto District School Board",
                                    "column": "school_board_name",
                                    "operator": "ILIKE"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "parks"
        ],
        "user_query": "Which parks have basketball courts?",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": [
                                "name",
                                "amenities",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "amenities",
                                    "operator": "ILIKE",
                                    "value": "%basketball%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "parks"
        ],
        "user_query": "List dog parks in the city",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "parks",
                            "columns": [
                                "name",
                                "amenities",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "amenities",
                                    "operator": "ILIKE",
                                    "value": "%dog%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "neighbourhoods"
        ],
        "user_query": "Show all neighbourhoods with classification 'Emerging'",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "neighbourhoods",
                            "columns": [
                                "area_name",
                                "classification",
                                "classification_code",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "classification_code",
                                    "operator": "=",
                                    "value": "EN"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "neighbourhoods"
        ],
        "user_query": "Show all neighbourhoods that are improvement areas",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "neighbourhoods",
                            "columns": [
                                "area_name",
                                "classification",
                                "classification_code",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "classification_code",
                                    "operator": "=",
                                    "value": "NIA"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "attractions"
        ],
        "user_query": "List all performing arts venues",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "category",
                                "address",
                                "description",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "category",
                                    "operator": "ILIKE",
                                    "value": "%performing arts%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "attractions"
        ],
        "user_query": "Where is the attraction Medieval Times?",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "attractions",
                            "columns": [
                                "name",
                                "category",
                                "address",
                                "description",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "name",
                                    "operator": "ILIKE",
                                    "value": "%medieval times%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "bike_lanes"
        ],
        "user_query": "Show protected bike lanes",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "bike_lanes",
                            "columns": [
                                "street_name",
                                "type",
                                "installed_year",
                                "upgraded_year",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "category",
                                    "operator": "NOT ILIKE",
                                    "value": "%sharrow%"
                                },
                                {
                                    "column": "category",
                                    "operator": "NOT ILIKE",
                                    "value": "%signed route%"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "type": "select_1.0",
        "sources": [
            "schools"
        ],
        "user_query": "List all public schools",
        "plan": {
            "action": "select",
            "groups": [
                {
                    "source_tables": [
                        {
                            "table": "schools",
                            "columns": [
                                "name",
                                "school_board_name",
                                "school_type",
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "value": "PR",
                                    "column": "school type",
                                    "operator": "NOT ILIKE"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
]

examples_pending_embed = []
