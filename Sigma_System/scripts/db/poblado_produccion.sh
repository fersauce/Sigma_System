#!/bin/bash
pg_restore -i -h localhost -p 5432 -U sigmasystem -d ss_des -v "poblado_tablas_produccion.backup"