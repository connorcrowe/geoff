#!/bin/bash
set -euo pipefail

: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${GEOFF_ETL_PASSWORD:?GEOFF_ETL_PASSWORD is required}"
: "${GEOFF_APP_PASSWORD:?GEOFF_APP_PASSWORD is required}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
-- Create roles using environment variables
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='user_etl') THEN
       CREATE ROLE user_etl LOGIN PASSWORD :'GEOFF_ETL_PASSWORD';
   END IF;
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='user_app') THEN
       CREATE ROLE user_app LOGIN PASSWORD :'GEOFF_APP_PASSWORD';
   END IF;
END
\$do\$;

-- Grant schema/table privileges
GRANT USAGE ON SCHEMA public TO user_etl;
GRANT USAGE ON SCHEMA public TO user_app;

GRANT CREATE ON SCHEMA public TO user_etl;
REVOKE CREATE ON SCHEMA public FROM user_app;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO user_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_etl;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user_etl;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO user_app;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO user_etl;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO user_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO user_etl;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO user_app;

-- Enable SQL logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET logging_collector = 'on';
SELECT pg_reload_conf();
EOSQL