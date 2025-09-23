# config/schema_keywords.py
"""Keyword lists for selecting relevant database tables for LLM prompt construction."""

schema_keywords = {
    "ambulance_stations": [
        "ambulance", "station", "ems", "emergency", "first response", "first responder"
        ],
    "bike_lanes": [
        "bike", "cycle", "bicycle", "lane", "lanes", "bikes", "route", "cycling", "cycle track", "path", "accessible", "active", "transportation"
        ],
    "fire_stations": [
        "fire", "fire truck", "station", "emergency", "first response", "first responder"
        ],
    "neighbourhoods": [
        "neighbourhoods", "neighbourhood", "community", "district", "area", "ward", "region", "neighborhood"
        ],
    "parking_lots": [
        "parking", "parking lot", "lot", "car", "park",
        ],
    "parks": [
        "park", "parks", "recreation", "rec", "green", "green space", "playground", "dog", "pool", "gym", "field", "community centre"
        ],
    "police_stations": [
        "police", "cop", "station", "enforcement", "law"
        ],
    "schools": [
        "school", "public", "private", "french", "english", "board", "education"
    ]
    # "streets": [
    #     "street", "road", "highway", "alley", "grid", "primary", "motorway", "track", "service", "path", "sidewalk", "pedestrian", "crossing", "lane", "speed", "traffic", "width", "roundabout"
    #     ]
}