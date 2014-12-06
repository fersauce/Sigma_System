#!/bin/bash
while true;#[ ${NUMERO} -ne "5" ];
do
    export NUMERO=$(zenity \
        --title="Por favor, digite la opción que desea realizar:" \
        --width 500 --height 240 --list --radiolist  \
        --column "Choose" --column "Option" TRUE "Reiniciar Servidor." \
        FALSE "Realizar Backup de Base de Datos de Producción." \
        FALSE "Realizar Backup de Base de Datos de Desarrollo." \
        FALSE "Restaurar copia de Base de Datos de Producción." \
        FALSE "Restaurar copia de Base de Datos de Desarrollo." \
        FALSE "Levantar un release en el servidor." \
        FALSE "Salir")
    echo ${NUMERO}
    case "$NUMERO" in
        "Reiniciar Servidor.")
            echo "# Reiniciando el servidor de aplicaciones."
            gksu service apache2 restart
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error \
                --text="Ha ocurrido un error al reiniciar el servidor";
            else
                zenity --width 300 --height 100 --info \
                --text="Servidor apache reiniciado con éxito"
            fi
        ;;
        "Realizar Backup de Base de Datos de Producción.")
            ./generar_backup_produccion.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error \
                --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info \
                --text="Backup realizado a la BD de Producción"
            fi
        ;;
        "Realizar Backup de Base de Datos de Desarrollo.")
            ./generar_backup_desarrollo.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error \
                --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info \
                --text="Backup realizado a la BD de Desarrollo"
            fi
        ;;
        "Restaurar copia de Base de Datos de Producción.")
            ./poblado_produccion.sh
        ;;
        "Restaurar copia de Base de Datos de Desarrollo.")
            ./poblado_desarrollo.sh
        ;;
        "Levantar un release en el servidor.")
            export DIR_LOCAL=$(pwd);
            cd /var/www/CRF_Project/;
            hola=$(git tag)
            export OPCIONES=""
            declare -i b=0;
            for h in ${hola};
            do
                if [ ${b} -eq 3 ];then
                OPCIONES=${OPCIONES}" FALSE "${h};
                else
                b=$(( b+1 ));
                fi
            done
            export GIT_OPCION=$(zenity \
                --title="Por favor, selecciona una versión:" --width 500 \
                --height 240 --list --radiolist \
                --column "Choose" --column "Option" ${OPCIONES});
            if [ "${GIT_OPCION}" != "Anterior" -a "${GIT_OPCION}" != "" ];then
                echo ${GIT_OPCION};
                gksu git stash;
                gksu git checkout ${GIT_OPCION};
                gksu service apache2 restart;
                cd ${DIR_LOCAL};
            fi
        ;;
        "Salir")
            break;
        ;;
        "")
            break;
        ;;
    esac
done