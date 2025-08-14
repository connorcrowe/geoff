import requests
import io
import pandas as pd

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
URL = BASE_URL + "/api/3/action/package_show"

def fetch_resource_ckan(package_id, resource_index=0):
    
    package = requests.get(URL, params={"id": package_id}).json()

    if not package.get("success"):
        raise RuntimeError(f"Failed to fetch package metadata: {package}")

    # Find first datastore_active resource
    resource_id = None
    for resource in package["result"]["resources"]:
        if resource.get("datastore_active"):
            resource_id = resource["id"]
            break

    # Get resource as csv
    dump_url = f"{BASE_URL}/datastore/dump/{resource_id}"
    resp = requests.get(dump_url)
    resp.raise_for_status()

    # Load into pandas
    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = [c.lower() for c in df.columns]
    return df, dump_url