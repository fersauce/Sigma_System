#!/bin/sh

pg_dump -i -h localhost -p 5432 -U postgres -F c -b -v -f "poblado_tablas_produccion.backup" ss_produccion