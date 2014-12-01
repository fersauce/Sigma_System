#!/bin/sh

echo "Comienza la generación del backup de la BD de producción del sistema" \
"Sigma_System"
cd backups_SS_prod/
pg_dump -i -h localhost -p 5432 -U postgres -F c -b -v -f \
    "poblado_tablas_produccion"$(date "+%y%m%d_%H%M%S")".backup" ss_produccion
echo "Backup culminado"