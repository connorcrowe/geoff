#!/bin/bash
set -euo pipefail

# Required env variables
: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${GEOFF_ETL_PASSWORD:?GEOFF_ETL_PASSWORD is required}"
: "${GEOFF_APP_PASSWORD:?GEOFF_APP_PASSWORD is required}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

-- 1. Create or update roles
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='user_etl') THEN
       CREATE ROLE user_etl LOGIN PASSWORD '${GEOFF_ETL_PASSWORD}';
   ELSE
       ALTER ROLE user_etl PASSWORD '${GEOFF_ETL_PASSWORD}';
   END IF;

   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='user_app') THEN
       CREATE ROLE user_app LOGIN PASSWORD '${GEOFF_APP_PASSWORD}';
   ELSE
       ALTER ROLE user_app PASSWORD '${GEOFF_APP_PASSWORD}';
   END IF;
END
\$do\$;

-- 2. ETL: full privileges on existing schemas/tables/sequences
GRANT ALL PRIVILEGES ON SCHEMA staging TO user_etl;
GRANT ALL PRIVILEGES ON SCHEMA data TO user_etl;
GRANT ALL PRIVILEGES ON SCHEMA meta TO user_etl;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO user_etl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA data TO user_etl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA meta TO user_etl;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA staging TO user_etl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA data TO user_etl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA meta TO user_etl;

-- 3. APP: read-only privileges on data schema
GRANT USAGE ON SCHEMA data TO user_app;
GRANT USAGE ON SCHEMA meta TO user_app;
GRANT SELECT ON ALL TABLES IN SCHEMA data TO user_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA data TO user_app;
GRANT SELECT ON ALL TABLES IN SCHEMA meta TO user_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA meta TO user_app;

-- 4. Default privileges for future tables/sequences created by ETL
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA data
    GRANT SELECT ON TABLES TO user_app;
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA data
    GRANT USAGE ON SEQUENCES TO user_app;
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA meta
    GRANT SELECT ON TABLES TO user_app;
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA meta
    GRANT USAGE ON SEQUENCES TO user_app;

ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA staging
    GRANT ALL ON TABLES TO user_etl;
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA staging
    GRANT ALL ON SEQUENCES TO user_etl;

ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA meta
    GRANT ALL ON TABLES TO user_etl;
ALTER DEFAULT PRIVILEGES FOR ROLE user_etl IN SCHEMA meta
    GRANT ALL ON SEQUENCES TO user_etl;

-- 5. Enable SQL logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET logging_collector = 'on';
SELECT pg_reload_conf();

EOSQL
