import csv
import json
import ast

INPUT_FILE = 'import/cycling-network-4326.csv'
OUTPUT_FILE = 'import/cleaned-bike-lanes.csv'

NULL_VALUES = {"", " ", "<Null>", ""}

def clean_value(value):
    return None if value.strip() in NULL_VALUES else value.strip()

def clean_geometry(value):
    try:
        # Parse broken JSON using ast.literal_eval
        parsed = ast.literal_eval(value)
        # Re-encode as valid JSON string
        return json.dumps(parsed)
    except Exception:
        return None

with open(INPUT_FILE, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        for key in row:
            if key == "geometry":
                row[key] = clean_geometry(row[key])
            else:
                row[key] = clean_value(row[key])
        writer.writerow(row)
