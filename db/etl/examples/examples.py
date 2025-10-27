examples_embedded = [
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
                                "school_type_desc"
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
                                "geometry"
                            ],
                            "filters": [
                                {
                                    "column": "classification_code",
                                    "operator": "ILIKE",
                                    "value": "%EN%"
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
    }
]

examples_pending_embed = []
