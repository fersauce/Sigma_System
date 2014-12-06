#!/bin/sh

echo "Comienza la generación del backup de la BD de desarrollo del sistema" \
"Sigma_System"
cd backups_SS_des/
pg_dump -i -h localhost -p 5432 -U sigmasystem -F c -b -v -f \
    "poblado_tablas_desarrollo"$(date "+%y%m%d_%H%M%S")".backup" ss_des
echo "Backup culminado"