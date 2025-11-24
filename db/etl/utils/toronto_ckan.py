import requests
import io
import pandas as pd
import zipfile

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
URL = BASE_URL + "/api/3/action/package_show"


def fetch_resource_ckan(package_id):
    package = requests.get(URL, params={"id": package_id}).json()
    if not package.get("success"):
        raise RuntimeError(f"Failed to fetch package metadata: {package}")

    resources = package["result"]["resources"]

    # 1. Try datastore resource first
    datastore_res = next((r for r in resources if r.get("datastore_active")), None)

    if datastore_res:
        resource_id = datastore_res["id"]
        dump_url = f"{BASE_URL}/datastore/dump/{resource_id}"
        resp = requests.get(dump_url)
        resp.raise_for_status()

        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = [c.lower() for c in df.columns]

        return df, dump_url

    # 2. Fall back to non-datastore resources
    file_res = next(
        (r for r in resources if r.get("url") and r.get("format", "").upper() in ["ZIP", "CSV", "JSON"]),
        None
    )

    if file_res is None:
        raise RuntimeError("No datastore or file resources found")

    url = file_res["url"]
    resp = requests.get(url)
    resp.raise_for_status()

    fmt = file_res.get("format", "").upper()

    # ZIP (like GTFS)
    if fmt == "ZIP":
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        dfs = {}

        for name in z.namelist():
            if not name.endswith(".txt"):
                continue

            raw = z.read(name)
            if len(raw.strip()) == 0:
                continue

            try:
                df = pd.read_csv(io.BytesIO(raw))
            except pd.errors.EmptyDataError:
                continue

            dfs[name] = df

        return dfs, url

    # CSV
    if fmt == "CSV":
        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = [c.lower() for c in df.columns]
        return df, url

    # JSON (rare but possible)
    if fmt == "JSON":
        return resp.json(), url

    raise RuntimeError(f"Unsupported resource format: {fmt}")
