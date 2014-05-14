#!/bin/bash
psql -h localhost -t -d ss_des -U sigmasystem -c "DROP SCHEMA public CASCADE;" > droptables

psql -h localhost -d ss_des -U sigmasystem -f droptables