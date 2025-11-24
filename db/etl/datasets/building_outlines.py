from utils.toronto_ckan import fetch_resource_ckan

# Specific package to fetch from CKAN Toronto
PACKAGE_ID = "topographic-mapping-building-outlines"

# Name for import table into staging database
TABLE_NAME = "building_outlines_raw"

def fetch():
    df, dump_url = fetch_resource_ckan(PACKAGE_ID)
    return df, TABLE_NAME, dump_url