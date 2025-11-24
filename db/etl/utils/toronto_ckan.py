import requests
import zipfile
import io
import pandas as pd

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
URL = BASE_URL + "/api/3/action/package_show"

def fetch_resource_ckan(package_id):
    package = requests.get(URL, params={"id": package_id}).json()
    if not package.get("success"):
        raise RuntimeError("Package not found")

    # Look for first downloadable resource
    resource = None
    for r in package["result"]["resources"]:
        if r.get("url") and r.get("format", "").upper() in ["ZIP", "CSV"]:
            resource = r
            break

    if resource is None:
        raise RuntimeError("No usable resource found")

    resp = requests.get(resource["url"])
    resp.raise_for_status()

    # If ZIP, extract files
    if resource["format"].upper() == "ZIP":
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        dfs = {}
        for name in z.namelist():
            if not name.endswith(".txt"):
                continue

            with z.open(name) as f:
                raw = f.read()
                if len(raw.strip()) == 0:
                    # Empty file, skip it
                    continue

                # Reset to file-like object for pandas
                f2 = io.BytesIO(raw)

                try:
                    df = pd.read_csv(f2)
                except pd.errors.EmptyDataError:
                    # Header-only file or malformed
                    continue

                dfs[name] = df
        return dfs, resource["url"]

    # If raw CSV
    else:
        df = pd.read_csv(io.StringIO(resp.text))
        return df, resource["url"]
