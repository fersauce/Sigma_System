import os, datetime


def loadTiposAtributos():
    """
    Script de carga de Tipos de Atributos del sistema.

    @author: Fernando Saucedo
    """

    #Se vacia la tabla
    Atributo.objects.all().delete()

    #Se agregan los nuevos valores
    Atributo.objects.create(
        tipo='Numerico',
        default='0'
    )
    Atributo.objects.create(
        tipo='Fecha',
        default=str(datetime.datetime.now())
    )
    Atributo.objects.create(
        tipo='Cadena',
        default=''
    )


if __name__ == '__main__':
    print 'Cargando Atributos...'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRF_Project.settings")
    from Sigma_System.models import Atributo
    loadTiposAtributos()