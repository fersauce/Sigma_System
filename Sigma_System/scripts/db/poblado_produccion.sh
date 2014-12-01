#!/bin/bash

export DIR_LOCAL=$(pwd);
cd backups_SS_prod;
hola=$(ls)
export OPCIONES=""
for h in ${hola};
do
    OPCIONES=${OPCIONES}" FALSE "${h};
done
export GIT_OPCION=$(zenity \
    --title="Por favor, selecciona una versión:" --width 500 \
    --height 240 --list --radiolist \
    --column "Choose" --column "Option" ${OPCIONES});
if [ "${GIT_OPCION}" != "" ];then
    echo "Borrando la BD de producción por completo";
    dropdb -i -h localhost -p 5432 -U sigmasystem ss_produccion;
    echo "Creando de nuevo la BD de producción";
    createdb -h localhost -p 5432 -U sigmasystem ss_produccion;
    echo "Iniciando la restauración del desde el backup seleccionado";
    pg_restore -i -h localhost -p 5432 -U sigmasystem -d ss_produccion \
        -v ${GIT_OPCION};
    if [ "$(echo $?)" -ne 0 ];then
        zenity --width 300 --height 100 --error \
        --text="Ha ocurrido un error";
    else
        zenity --width 300 --height 100 --info \
        --text="Restauración realizada a la BD de Producción."
    fi
fi
cd ${DIR_LOCAL};
