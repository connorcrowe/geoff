from utils.toronto_ckan import fetch_resource_ckan

# Specific package to fetch from CKAN Toronto
PACKAGE_ID = "merged-gtfs-ttc-routes-and-schedules"

# Name for import table into staging database
TABLE_PREFIX = "gtfs"

def fetch():
    dfs, dump_url = fetch_resource_ckan(PACKAGE_ID)
  
    return dfs, TABLE_PREFIX, dump_url