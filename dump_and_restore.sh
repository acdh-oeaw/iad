rm dump.sql
pg_dump -d iad -h 127.0.0.1 -p 5433 -U iad -c -f dump.sql
psql --username=postgres --dbname=iad  --port=5432
\ir dump.sql