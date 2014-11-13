#!/bin/bash
while true;#[ ${NUMERO} -ne "5" ];
do
    export NUMERO=$(zenity --title="Por favor, digite la opción que desea realizar:" \
        --width 500 --height 240 --list --radiolist  --column "Choose" \
        --column "Option" TRUE "Reiniciar Servidor." \
        FALSE "Realizar Backup de Base de Datos de Producción." \
        FALSE "Realizar Backup de Base de Datos de Desarrollo." \
        FALSE "Restaurar copia de Base de Datos de Producción." \
        FALSE "Restaurar copia de Base de Datos de Desarrollo." \
        FALSE "Levantar un release en el servidor." \
        FALSE "Salir")
    echo ${NUMERO}
    case "$NUMERO" in
        "Reiniciar Servidor.")
            echo "# Iniciando"
            gksu service apache2 restart
            #zenity --text="Espere mientras se reinicia el servidor" --progress --auto-close --auto-kill --percentage=0
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error --text="Ha ocurrido un error al reiniciar el servidor";
            else
                zenity --width 300 --height 100 --info --text="Servidor apache reiniciado con éxito"
            fi
        ;;
        "Realizar Backup de Base de Datos de Producción.")
            ./generar_backup_produccion.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info --text="Backup realizado a la BD de Producción"
            fi
        ;;
        "Realizar Backup de Base de Datos de Desarrollo.")
            ./generar_backup_desarrollo.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info --text="Backup realizado a la BD de Desarrollo"
            fi
        ;;
        "Restaurar copia de Base de Datos de Producción.")
            ./borrado_produccion.sh
            echo "BD de producción borrada."
            ./poblado_produccion.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info --text="Backup realizada a la BD de Producción"
            fi
        ;;
        "Restaurar copia de Base de Datos de Desarrollo.")
            ./borrado_desarrollo.sh
            echo "BD de desarrollo borrada."
            ./poblado_desarrollo.sh
            if [ "$(echo $?)" -ne 0 ];then
                zenity --width 300 --height 100 --error --text="Ha ocurrido un error";
            else
                zenity --width 300 --height 100 --info --text="Restauración realizada a la BD de Desarrollo"
            fi
        ;;
        "Levantar un release en el servidor.")
            hola=$(git tag)
            export OPCIONES=""
            for h in ${hola};
            do
                OPCIONES=${OPCIONES}" FALSE "${h};
            done
            export NUMERO=$(zenity --title="Por favor, digite la opción que desea realizar:" \
                --width 500 --height 240 --list --radiolist  --column "Choose" \
                --column "Option" ${OPCIONES}
                FALSE "Salir")
                echo ${NUMERO};
        ;;
        "Salir")
            break
        ;;
    esac
done