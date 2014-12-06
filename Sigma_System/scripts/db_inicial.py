import os
import datetime


__author__ = 'fernando'


def loadUsuarios():
    user = User.objects.all().order_by('id')[0]

    Usuario.objects.create(user=user, ci="__12345__", direccion="", tel="",
                           estado=True)

    usuario = User.objects.create(username='fsaucedo',
                                  first_name='Fernando',
                                  last_name='Saucedo',
                                  email='carlifer.fernando@gmail.com',
                                  password=make_password(
                                      'fsaucedo'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='4083917',
                           direccion='Villa Elisa',
                           tel='(021) 940-845',
                           estado=True)
    usuario = User.objects.create(username='ccandia',
                                  first_name='Cristian',
                                  last_name='Candia',
                                  email='kandia88@gmail.com',
                                  password=make_password(
                                      'ccandia'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='1234567',
                           direccion='Lambare',
                           tel='(0961) 891-325',
                           estado=True)
    usuario = User.objects.create(username='rcenturion',
                                  first_name='Ruth',
                                  last_name='Centurion',
                                  email='ruthiccr@gmail.com',
                                  password=make_password(
                                      'rcenturion'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='7654321',
                           direccion='Limpio',
                           tel='(0985) 123-456',
                           estado=True)
    usuario = User.objects.create(username='ggonzalez',
                                  first_name='Guillermo',
                                  last_name='Gonzalez',
                                  email='ggonzalez@pol.una.py',
                                  password=make_password(
                                      'ggonzalez'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='3316547',
                           direccion='Asuncion',
                           tel='(0985) 845-315',
                           estado=True)
    usuario = User.objects.create(username='ebanuelos',
                                  first_name='Enrique',
                                  last_name='Banhuelos',
                                  email='ebanuelos@gmail.com',
                                  password=make_password(
                                      'ebanuelos'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='451258',
                           direccion='Fernando de la Mora',
                           tel='(0972) 512-697',
                           estado=True)
    usuario = User.objects.create(username='jmesquita',
                                  first_name='Jorge',
                                  last_name='Mesquita',
                                  email='ja1990@gmail.com',
                                  password=make_password(
                                      'jmesquita'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='4521686',
                           direccion='Asuncion',
                           tel='(0961) 458-921',
                           estado=True)
    usuario = User.objects.create(username='jsalcedo',
                                  first_name='Jean',
                                  last_name='Salcedo',
                                  email='jloncha@gmail.com',
                                  password=make_password(
                                      'jloncha'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='4521485',
                           direccion='Yaguaron',
                           tel='(0421) 985-321',
                           estado=True)
    usuario = User.objects.create(username='kpistilli',
                                  first_name='Klaus',
                                  last_name='Pistilli',
                                  email='kpistilli@gmail.com',
                                  password=make_password(
                                      'kpistilli'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='',
                           direccion='Luque',
                           tel='(0981) 452-932',
                           estado=True)
    usuario = User.objects.create(username='kosorio',
                                  first_name='Guillermo',
                                  last_name='Osorio',
                                  email='kike.osorio@gmail.com',
                                  password=make_password(
                                      'kosorio'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='3584623',
                           direccion='San Lorenzo',
                           tel='(0981) 542-685',
                           estado=True)
    usuario = User.objects.create(username='vfranco',
                                  first_name='Victor',
                                  last_name='Franco',
                                  email='victorfranco90@gmail.com',
                                  password=make_password(
                                      'vfranco'),
                                  is_active=True)
    Usuario.objects.create(user=usuario, ci='3444638',
                           direccion='San Lorenzo',
                           tel='(0961) 368-594',
                           estado=True)

    print 'Se cargaron correctamente los usuarios.'


def loadPermisos():
    # Se vacia la tabla rol
    Rol.objects.all().delete()

    # Se establecen los roles por defecto
    rol_adm_sistema = Rol.objects.create(nombre="Administrador de Sistema",
                                         descripcion="Con este rol se establece"
                                                     " el superusuario con "
                                                     "todos los permisos del "
                                                     "sistema asignados")

    rol_lider = Rol.objects.create(nombre="Lider",
                                   descripcion="Rol que posibilita "
                                               "administrar completamente "
                                               "un proyecto")

    rol_desarrollador = Rol.objects.create(nombre="Desarrollador",
                                           descripcion="Rol que posibilita "
                                                       "desarrollar un "
                                                       "proyecto")

    # Se vacia la tabla permiso
    Permiso.objects.all().delete()

    # Se cargan todos los permisos y se asignan a los roles.
    p = Permiso.objects.create(nombre="Super Usuario", codigo="super_us")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Usuario", codigo="crear_us")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Modificar Usuario",
                               codigo="modificar_us")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Usuario", codigo="eliminar_us")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Usuario", codigo="ver_us")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Rol", codigo="crear_rol")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Modificar Rol", codigo="modificar_rol")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Rol", codigo="eliminar_rol")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Rol", codigo="ver_rol")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Proyecto", codigo="crear_pr")
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Modificar Proyecto",
                               codigo="modificar_pr")
    rol_adm_sistema.permisos.add(p)
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Proyecto", codigo="eliminar_pr")
    rol_lider.permisos.add(p)
    rol_adm_sistema.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Proyecto", codigo="ver_pr")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Fase", codigo="crear_fa")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Modificar Fase", codigo="modificar_fa")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Fase", codigo="eliminar_fa")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Fase", codigo="ver_fa")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Tipo de Item", codigo="crear_ti")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Modificar Tipo de Item",
                               codigo="modificar_ti")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Tipo de Item",
                               codigo="eliminar_ti")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Tipo de Item", codigo="eliminar_ti")
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Item", codigo="crear_item")
    rol_desarrollador.permisos.add(p)

    p = Permiso.objects.create(nombre="Modificar Item", codigo="modificar_item")
    rol_desarrollador.permisos.add(p)
    p = Permiso.objects.create(nombre="Eliminar Item", codigo="eliminar_item")
    rol_desarrollador.permisos.add(p)
    p = Permiso.objects.create(nombre="Ver Item", codigo="ver_item")
    rol_desarrollador.permisos.add(p)
    p = Permiso.objects.create(nombre="Crear Linea Base", codigo="crear_lb")
    rol_desarrollador.permisos.add(p)
    p = Permiso.objects.create(nombre="Votar", codigo="votar")
    rol_desarrollador.permisos.add(p)
    rol_lider.permisos.add(p)
    p = Permiso.objects.create(nombre="Realizar Solicitud", codigo="real_solic")
    rol_desarrollador.permisos.add(p)
    rol_lider.permisos.add(p)

    user = User.objects.all().order_by('id')[0]
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_adm_sistema,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='fsaucedo')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_lider,
                              idProyecto=0, idFase=0, idItem=0)
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='ccandia')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_lider,
                              idProyecto=0, idFase=0, idItem=0)
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='rcenturion')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_lider,
                              idProyecto=0, idFase=0, idItem=0)
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='kpistilli')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='kosorio')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='ebanuelos')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='ggonzalez')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)
    user = User.objects.get(username='vfranco')
    UsuarioRol.objects.create(usuario=user.usuario, rol=rol_desarrollador,
                              idProyecto=0, idFase=0, idItem=0)

    print("Se cargaron correctamente los roles")


def loadTiposAtributos():
    """
    Script de carga de Tipos de Atributos del sistema.

    @author: Fernando Saucedo
    """

    # Se vacia la tabla
    Atributo.objects.all().delete()

    # Se agregan los nuevos valores
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


def loadProyectos():
    """
    Script para cargar los proyectos, uno a iniciar, otro iniciado y otro a
    finalizar
    :return:
    """
    proyectoInicial = Proyecto.objects.create(nombre='Iniciar',
                                              fechaCreacion=datetime.datetime.now(),
                                              descripcion='Proyecto a iniciar',
                                              complejidad=0,
                                              costo=0,
                                              estado='Pendiente',
                                              nroFases=4,
                                              nroMiembros=1,
                                              duracion=0,
                                              fechaInicio=datetime.datetime.now(),
                                              fechaFinalizacion=datetime.datetime.now() + datetime.timedelta(
                                                  days=10))
    comite = Comite.objects.create(obs='Comite Numero 1',
                                   nro_integ=3,
                                   fecha_creacion=datetime.datetime.now(),
                                   proy=proyectoInicial)
    user = User.objects.get(username='fsaucedo')
    UsuariosXProyecto.objects.create(proyecto=proyectoInicial,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=True)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='rcenturion')
    UsuariosXProyecto.objects.create(proyecto=proyectoInicial,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='ccandia')
    UsuariosXProyecto.objects.create(proyecto=proyectoInicial,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='vfranco')
    UsuariosXProyecto.objects.create(proyecto=proyectoInicial,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    user = User.objects.get(username='kosorio')
    UsuariosXProyecto.objects.create(proyecto=proyectoInicial,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)

    proyectoIniciado = Proyecto.objects.create(nombre='Iniciado',
                                               fechaCreacion=datetime.datetime.now(),
                                               descripcion='Proyecto iniciado',
                                               complejidad=0,
                                               costo=0,
                                               estado='Pendiente',
                                               nroFases=4,
                                               nroMiembros=1,
                                               duracion=0,
                                               fechaInicio=datetime.datetime.now(),
                                               fechaFinalizacion=datetime.datetime.now() + datetime.timedelta(
                                                   days=10))
    comite = Comite.objects.create(obs='Comite Numero 2',
                                   nro_integ=3,
                                   fecha_creacion=datetime.datetime.now(),
                                   proy=proyectoIniciado)
    user = User.objects.get(username='fsaucedo')
    UsuariosXProyecto.objects.create(proyecto=proyectoIniciado,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    user = User.objects.get(username='rcenturion')
    UsuariosXProyecto.objects.create(proyecto=proyectoIniciado,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='ccandia')
    UsuariosXProyecto.objects.create(proyecto=proyectoIniciado,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=True)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='vfranco')
    UsuariosXProyecto.objects.create(proyecto=proyectoIniciado,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='kosorio')
    UsuariosXProyecto.objects.create(proyecto=proyectoIniciado,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)

    fase1 = Fase.objects.create(proyecto=proyectoIniciado,
                                nombre='fase1',
                                descripcion='Fase 1',
                                posicionFase=Fase.objects.filter(
                                    proyecto=proyectoIniciado).__len__() + 1,
                                estado='Pendiente',
                                fechaInicio=proyectoIniciado.fechaInicio,
                                fechaFin=datetime.datetime.now() + datetime.timedelta(
                                    days=1))
    fase2 = Fase.objects.create(proyecto=proyectoIniciado,
                                nombre='fase1',
                                descripcion='Fase 1',
                                posicionFase=Fase.objects.filter(
                                    proyecto=proyectoIniciado).__len__() + 1,
                                estado='Pendiente',
                                fechaInicio=proyectoIniciado.fechaInicio,
                                fechaFin=datetime.datetime.now() + datetime.timedelta(
                                    days=1))
    fase3 = Fase.objects.create(proyecto=proyectoIniciado,
                                nombre='fase1',
                                descripcion='Fase 1',
                                posicionFase=Fase.objects.filter(
                                    proyecto=proyectoIniciado).__len__() + 1,
                                estado='Pendiente',
                                fechaInicio=proyectoIniciado.fechaInicio,
                                fechaFin=datetime.datetime.now() + datetime.timedelta(
                                    days=1))
    fase4 = Fase.objects.create(proyecto=proyectoIniciado,
                                nombre='fase1',
                                descripcion='Fase 1',
                                posicionFase=Fase.objects.filter(
                                    proyecto=proyectoIniciado).__len__() + 1,
                                estado='Pendiente',
                                fechaInicio=proyectoIniciado.fechaInicio,
                                fechaFin=datetime.datetime.now() + datetime.timedelta(
                                    days=1))
    proyectoFinalizar = Proyecto.objects.create(nombre='Finalizar',
                                                fechaCreacion=datetime.datetime.now(),
                                                descripcion='Proyecto a finalizar',
                                                complejidad=0,
                                                costo=0,
                                                estado='Pendiente',
                                                nroFases=3,
                                                nroMiembros=1,
                                                duracion=0,
                                                fechaInicio=datetime.datetime.now(),
                                                fechaFinalizacion=datetime.datetime.now() + datetime.timedelta(
                                                    days=10))
    comite = Comite.objects.create(obs='Comite Numero 3',
                                   nro_integ=3,
                                   fecha_creacion=datetime.datetime.now(),
                                   proy=proyectoFinalizar)
    user = User.objects.get(username='fsaucedo')
    UsuariosXProyecto.objects.create(proyecto=proyectoFinalizar,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='rcenturion')
    UsuariosXProyecto.objects.create(proyecto=proyectoFinalizar,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=True)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)
    user = User.objects.get(username='ccandia')
    UsuariosXProyecto.objects.create(proyecto=proyectoFinalizar,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    user = User.objects.get(username='vfranco')
    UsuariosXProyecto.objects.create(proyecto=proyectoFinalizar,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    user = User.objects.get(username='kosorio')
    UsuariosXProyecto.objects.create(proyecto=proyectoFinalizar,
                                     usuario=user.usuario,
                                     activo=True,
                                     lider=False)
    UsuarioPorComite.objects.create(comite=comite,
                                    usuario=user)


# Empieza la ejecucion
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRF_Project.settings")
    from django.contrib.auth.hashers import make_password
    from django.contrib.auth.models import User
    from Sigma_System.models import Usuario, Atributo, Permiso, Rol, UsuarioRol, \
        Proyecto, UsuariosXProyecto, Fase, Comite, UsuarioPorComite

    print 'Cargando usuarios'
    loadUsuarios()
    print "Cargando permisos..."
    loadPermisos()
    print 'Cargando Tipos de Atributos'
    loadTiposAtributos()