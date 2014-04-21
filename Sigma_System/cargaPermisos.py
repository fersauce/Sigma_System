__author__ = 'cristian'
import os

def loadPermisos():

    #Se vacia la tabla permiso
    Permiso.objects.all().delete()

    #Se cargan todos los permisos
    Permiso.objects.create(id=1, nombre="Crear Usuario", codigo="crear_us")
    Permiso.objects.create(id=2, nombre="Modificar Usuario", codigo="modificar_us")
    Permiso.objects.create(id=3, nombre="Eliminar Usuario", codigo="eliminar_us")

    Permiso.objects.create(id=4, nombre="Crear Rol", codigo="crear_ro")
    Permiso.objects.create(id=5, nombre="Modificar Rol", codigo="modificar_ro")
    Permiso.objects.create(id=6, nombre="Eliminar Rol", codigo="eliminar_ro")

    Permiso.objects.create(id=7, nombre="Crear Proyecto", codigo="crear_pr")
    Permiso.objects.create(id=8, nombre="Modificar Proyecto", codigo="modificar_pr")
    Permiso.objects.create(id=9, nombre="Eliminar Proyecto", codigo="eliminar_pr")

    Permiso.objects.create(id=10, nombre="Crear Proyecto", codigo="crear_pr")
    Permiso.objects.create(id=11, nombre="Modificar Proyecto", codigo="modificar_pr")
    Permiso.objects.create(id=12, nombre="Eliminar Proyecto", codigo="eliminar_pr")

    Permiso.objects.create(id=13, nombre="Crear Fase", codigo="crear_fa")
    Permiso.objects.create(id=14, nombre="Modificar Fase", codigo="modificar_fa")
    Permiso.objects.create(id=15, nombre="Eliminar Fase", codigo="eliminar_fa")

    Permiso.objects.create(id=16, nombre="Crear Tipo de Item", codigo="crear_ti")
    Permiso.objects.create(id=17, nombre="Modificar Tipo de Item", codigo="modificar_ti")
    Permiso.objects.create(id=18, nombre="Eliminar Tipo de Item", codigo="eliminar_ti")

    Permiso.objects.create(id=19, nombre="Crear Item", codigo="crear_item")
    Permiso.objects.create(id=20, nombre="Modificar Item", codigo="modificar_item")
    Permiso.objects.create(id=21, nombre="Eliminar Item", codigo="eliminar_item")

    Permiso.objects.create(id=22, nombre="Crear Linea Base", codigo="crear_lb")

    Permiso.objects.create(id=23, nombre="Votar", codigo="votar")

    Permiso.objects.create(id=24, nombre="Realizar Solicitud", codigo="real_solic")

    #Se vacia la tabla rol
    Rol.objects.all().delete()

    #Se establecen los roles por defecto
    rol_adm_sistema = Rol.objects.create(id=1, nombre="Administrador de Sistema",
                                       descripcion="Con este rol se establece el superusuario con todos los"
                                                   "permisos del sistema asignados")

    rol_adm_proy = Rol.objects.create(id=2, nombre="Administrador de Proyecto",
                                       descripcion="Rol que posibilita administrar completamente un proyecto")

    rol_adm_fase = Rol.objects.create(id=3, nombre="Administrador de Fase",
                                       descripcion="Rol que posibilita administrar completamente una fase")

            # Se imprimen los permisos cargados
    for p in Permiso.objects.all():
        rol_adm_sistema.permisos.add(p)
        rol_adm_proy.permisos.add(p)
        rol_adm_fase.permisos.add(p)
        print p.nombre
    Rol.objects.get(id=2).delete()
    Rol.objects.get(id=3).delete()
    print("Se cargaron correctamente los roles")

# Empieza la ejecucion
if __name__ == '__main__':
    print "Cargando permisos..."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRF_Project.settings")
    from Sigma_System.models import Permiso, Rol
    loadPermisos()