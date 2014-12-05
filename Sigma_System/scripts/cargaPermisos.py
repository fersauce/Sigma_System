import os


def loadPermisos():
    # Se vacia la tabla permiso
    Permiso.objects.all().delete()

    # Se cargan todos los permisos
    Permiso.objects.create(nombre="Super Usuario", codigo="super_us")

    Permiso.objects.create(nombre="Crear Usuario", codigo="crear_us")
    Permiso.objects.create(nombre="Modificar Usuario", codigo="modificar_us")
    Permiso.objects.create(nombre="Eliminar Usuario", codigo="eliminar_us")
    Permiso.objects.create(nombre="Ver Usuario", codigo="ver_us")

    Permiso.objects.create(nombre="Crear Rol", codigo="crear_rol")
    Permiso.objects.create(nombre="Modificar Rol", codigo="modificar_rol")
    Permiso.objects.create(nombre="Eliminar Rol", codigo="eliminar_rol")
    Permiso.objects.create(nombre="Ver Rol", codigo="ver_rol")

    Permiso.objects.create(nombre="Crear Proyecto", codigo="crear_pr")
    Permiso.objects.create(nombre="Modificar Proyecto", codigo="modificar_pr")
    Permiso.objects.create(nombre="Eliminar Proyecto", codigo="eliminar_pr")
    Permiso.objects.create(nombre="Ver Proyecto", codigo="ver_pr")

    Permiso.objects.create(nombre="Crear Fase", codigo="crear_fa")
    Permiso.objects.create(nombre="Modificar Fase", codigo="modificar_fa")
    Permiso.objects.create(nombre="Eliminar Fase", codigo="eliminar_fa")
    Permiso.objects.create(nombre="Ver Fase", codigo="ver_fa")

    Permiso.objects.create(nombre="Crear Tipo de Item", codigo="crear_ti")
    Permiso.objects.create(nombre="Modificar Tipo de Item",
                           codigo="modificar_ti")
    Permiso.objects.create(nombre="Eliminar Tipo de Item", codigo="eliminar_ti")
    Permiso.objects.create(nombre="Ver Tipo de Item", codigo="eliminar_ti")

    Permiso.objects.create(nombre="Crear Item", codigo="crear_item")
    Permiso.objects.create(nombre="Modificar Item", codigo="modificar_item")
    Permiso.objects.create(nombre="Eliminar Item", codigo="eliminar_item")
    Permiso.objects.create(nombre="Ver Item", codigo="ver_item")

    Permiso.objects.create(nombre="Crear Linea Base", codigo="crear_lb")

    Permiso.objects.create(nombre="Votar", codigo="votar")

    Permiso.objects.create(nombre="Realizar Solicitud", codigo="real_solic")

    #Se vacia la tabla rol
    Rol.objects.all().delete()

    #Se establecen los roles por defecto
    rol_adm_sistema = Rol.objects.create(nombre="Administrador de Sistema",
                                         descripcion="Con este rol se establece el superusuario con todos los"
                                                     "permisos del sistema asignados")

    rol_adm_proy = Rol.objects.create(nombre="Administrador de Proyecto",
                                      descripcion="Rol que posibilita administrar completamente un proyecto")

    rol_adm_fase = Rol.objects.create(nombre="Administrador de Fase",
                                      descripcion="Rol que posibilita administrar completamente una fase")

    # Se imprimen los permisos cargados
    for p in Permiso.objects.all():
        rol_adm_sistema.permisos.add(p)
        rol_adm_proy.permisos.add(p)
        rol_adm_fase.permisos.add(p)
        print p.nombre
    Rol.objects.get(id=rol_adm_proy.id).delete()
    Rol.objects.get(id=rol_adm_fase.id).delete()

    user = User.objects.all().order_by('id')[0]
    Usuario.objects.create(user=user, ci="__12345__", direccion="", tel="",
                           estado=True)

    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_adm_sistema,
                              idProyecto=0, idFase=0, idItem=0)

    print("Se cargaron correctamente los roles")


# Empieza la ejecucion
if __name__ == '__main__':
    print "Cargando permisos..."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRF_Project.settings")
    from Sigma_System.models import Permiso, Rol, UsuarioRol, Usuario
    from django.contrib.auth.models import User

    '''rol_adm_fase = Rol.objects.create(nombre="Administrador de Fase",
                                       descripcion="Rol que posibilita administrar completamente una fase")
    user = User.objects.all().order_by('id')[1]

    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_adm_fase, idProyecto=0, idFase=0, idItem=0)'''
    # print user.usuario.roles
    # for r in user.usuario.roles.all():
    #    print r.nombre
    #usuario.roles.add(rol_adm_sistema)
    loadPermisos()