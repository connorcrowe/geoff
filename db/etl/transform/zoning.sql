DROP TABLE IF EXISTS data.zoning;
CREATE TABLE data.zoning AS
SELECT
    --CAST(_id AS integer) AS id,
    --NULLIF(some_string, '')::text AS name,
    --CAST(some_int AS integer) AS location_id,
    --ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry

    CAST(_id AS integer) AS id,
    NULLIF(zn_zone, '')::text AS zone,
    CAST(gen_zone AS integer) AS zone_code,
    CAST(units AS integer) AS max_units,
    NULLIF(zn_string, '')::text AS full_zone_string,
    NULLIF(zbl_excptn, '')::text AS zoning_exception,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.zoning_raw;

ALTER TABLE data.zoning ADD PRIMARY KEY (id);
CREATE INDEX ON data.zoning USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.zoning.id IS 'Unique identifier';
COMMENT ON COLUMN data.zoning.zone IS 'Name of the zone. R: Residential, RD: Residential Detached, RS: Residential Semi-Detached, RM: Residential multiple, RA: Residential Apartment, RAC: Residential Apartment Commercial, O: Open Space, ON: Open Space Natural, OR: Open Space Recreation, UT: Utility & Transport, CL: Commercial Local, CR: Commerical Residential, CRE: Commercial Residential Employment, EL: Employment Light Industrial, E: Employment industrial, EH: Employment Heavy Industrial, EO: Employment Office, I: Institutional, IH: Institutional Hospital, IE: Institutional Education, IS: Institutional School';
COMMENT ON COLUMN data.zoning.zone_code IS 'Zoned destination of the zone limited by GEN_ZONE. 0 = Residential 1 = Open Space 2 = Utility and Transportation 4 = Employment Industrial 5 = Institutional 6 = Commercial Residential Employment 101 = Residential Apartment 201 = Commercial 202 = Commercial Residential ';
COMMENT ON COLUMN data.zoning.max_units IS '	The permitted maximum number of Dwelling Units allowed on a lot in the zone, and is a numeric value prefaced by the letter u in a residential zone.';
COMMENT ON COLUMN data.zoning.full_zone_string IS 'Complete label of the zone.';
COMMENT ON COLUMN data.zoning.zoning_exception IS 'This indicates whether a zone has an Exception. Yes (Y) or No (N)';
COMMENT ON COLUMN data.zoning.geometry IS 'Geometry: polygon location of the zone';
