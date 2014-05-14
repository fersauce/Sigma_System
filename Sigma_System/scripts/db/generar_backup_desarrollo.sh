#!/bin/sh

pg_dump -i -h localhost -p 5432 -U sigmasystem -F c -b -v -f "poblado_tablas_desarrollo.backup" ss_des