#!/bin/bash
psql -h localhost -t -d ss_produccion -U sigmasystem -c "DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
" > droptables

psql -h localhost -d ss_produccion -U sigmasystem -f droptables