#!/bin/bash

pg_dump -d iad -h localhost -p 5433 -U  iad -c -f iad_dump.sql
psql -U postgres -d iad < iad_dump.sql
