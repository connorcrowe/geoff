# config/schema_keywords.py
"""Keyword lists for selecting relevant database tables for LLM prompt construction."""

schema_keywords = {
    "bike_lanes": [
        "bike", "cycle", "bicycle", "lane", "lanes", "bikes", "route", "cycling", "cycle track", "path", "accessible", "active", "transportation"
        ],
    "neighbourhoods": [
        "neighbourhoods", "neighbourhood", "community", "district", "area", "ward", "region", "neighborhood"
        ],
    "parks": [
        "park", "parks", "recreation", "rec", "green", "green space", "playground", "dog", "pool", "gym", "field"
        ]
}