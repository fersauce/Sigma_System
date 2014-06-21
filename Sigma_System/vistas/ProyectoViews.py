from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
import simplejson
import sys
from Sigma_System.forms import BusquedaProyectoForm, AltaProyectoForm
from Sigma_System.models import Proyecto, Usuario, Fase, UsuariosXProyecto, \
    UsuarioRol, Rol, Comite, UsuarioPorComite
import datetime, time
from Sigma_System.decoradores import permisos_requeridos
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def administrar_proyecto(request):
    """
    Vista para acceder a la administracion de proyectos.
    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    permisos = request.session['permisos']
    usuario = request.user.usuario
    proyectos = usuario.proyectos.all()
    if 'super_us' in permisos:
        proyectos = Proyecto.objects.all().order_by('-nombre')
    elif 'modificar_pr' in permisos:
        usu_proyectos = UsuariosXProyecto.objects.filter(usuario=request.user.usuario, activo=True)
        permisos = request.session['permisos']
        proyectos = []
        for u in usu_proyectos:
            proyectos.append(u.proyecto)
    return render(request, 'administrarproyectos.html',
                  {'proyectos': proyectos,
                   'vacio': 'No se encuentran proyectos registrados',
                   'form': BusquedaProyectoForm(),
                   'permisos': permisos})


@login_required(login_url='/login/')
@permisos_requeridos(['crear_pr'], 'sigma: adm_proy', 'crear proyectos')
def alta_proyecto(request):
    """
    Vista que realiza la creacion de un nuevo proyecto
    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    rol = Rol.objects.filter(nombre='Lider').first()
    print rol
    lideres = UsuarioRol.objects.filter(rol__pk=rol.pk)
    if request.method == 'POST':
        proyecto = Proyecto.objects.filter(
            nombre=request.POST['nombreProyecto'])
        if not proyecto:
            fecha = datetime.datetime.now()
            try:
                tl = Usuario.objects.get(pk=request.POST['lider'])
                print tl.user.username
                nuevoProyecto = Proyecto(
                    nombre=request.POST['nombreProyecto'],
                    fechaCreacion=fecha,
                    descripcion=request.POST['descripcion'],
                    complejidad=0,
                    costo=0,
                    estado='Pendiente',
                    nroFases=request.POST['nroFases'],
                    nroMiembros=1,
                    duracion=0,
                    fechaInicio=datetime.datetime.now(),
                    fechaFinalizacion=datetime.datetime.now() + datetime.timedelta(
                        days=10)
                )
                nuevoProyecto.save()
                lider = UsuariosXProyecto(
                    proyecto=nuevoProyecto,
                    usuario=tl,
                    activo=True,
                    lider=True
                )
                lider.save()
                '''usuarios = Usuario.objects.all().exclude(pk=tl.pk)
                for usuario in usuarios:
                    UsuariosXProyecto.objects.create(
                        proyecto=nuevoProyecto,
                        usuario=usuario
                    )'''
                comite = Comite.objects.create(
                    obs='Comite de cambios del proyecto ' +
                        nuevoProyecto.nombre + '',
                    nro_integ=1,
                    fecha_creacion=datetime.datetime.now(),
                    proy=nuevoProyecto
                )
                UsuarioPorComite.objects.create(
                    comite=comite,
                    usuario=tl
                )
                messages.success(request, 'Proyecto ' + str(
                    nuevoProyecto.nombre) + ' creado con exito')
            except Exception as error:
                messages.error(request, 'Ocurrio un error al crear el '
                                        'proyecto')
                print error.args
                print sys.exc_info()
            return HttpResponseRedirect(reverse('sigma:adm_proy'))
        else:
            messages.error(request,
                           'No se pudo crear el proyecto: El nombre ya '
                           'existe en el sistema.')
            return render(request, 'proyectoalta.html', {'lideres': lideres})
    return render_to_response('proyectoalta.html', {'lideres': lideres},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permisos_requeridos(['modificar_pr'], 'sigma:adm_proy', 'modificar proyectos')
def modificar_proyecto(request, idProyecto):
    """
    Vista para realizar la modificacion de datos del proyecto
    """
    proyecto = Proyecto.objects.get(pk=idProyecto)
    if request.method == 'POST':
        if proyecto.estado == 'Iniciado':
            messages.error(request, 'No se puede modificar mas, ya que el '
                                    'proyecto ya se ha iniciado.')
        else:
            list_proyecto = Proyecto.objects.exclude(pk=idProyecto)
            for proy in list_proyecto:
                if proy.nombre == request.POST['nombre']:
                    messages.error(request, 'El nombre de ese proyecto ya '
                                            'existe, escriba otro')
                    return render(request, 'proyectomodificar.html',
                                  {'proyecto': proyecto})
            proyecto.nombre = request.POST['nombre']
            proyecto.descripcion = request.POST['descripcion']
        try:
            proyecto.save()
        except Exception as error:
            messages.error(request, 'Ocurrio un error al intentar modificar '
                                    'el proyecto')
            return render(request, 'proyectomodificar.html',
                          {'proyecto': proyecto})
        return HttpResponseRedirect('/ss/proyecto')
    return render(request, 'proyectomodificar.html', {'proyecto': proyecto})


@login_required(login_url='/login/')
@permisos_requeridos(['eliminar_pr'], 'sigma:adm_proy', 'eliminar proyectos')
def baja_proyecto(request, idProyecto):
    """
    Vista para realizar la baja de un proyecto.
    :param idProyecto: pk del proyecto a ser suprimido del sistema.
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyecto)
        if proyecto.estado == 'Iniciado':
            messages.error(request, 'No se puede suprimir el proyecto: ya esta '
                                    'iniciado')
        elif Fase.objects.filter(proyecto=proyecto).__len__() > 0:
            messages.error(request, 'No se puede suprimir el proyecto: '
                                    'tiene fases creadas')
        else:
            try:
                nombre = proyecto.nombre
                proyecto.delete()
                messages.success(request,
                                 'Proyecto ' + str(nombre) + ' eliminado')
            except Exception as error:
                messages.error(request, 'Ocurrio un error al intentar suprimir'
                                        'el proyecto.')
    return HttpResponseRedirect(reverse('sigma:adm_proy'))


def buscar_proyecto(request):
    """
    Vista para realizar la busqueda de un proyecto
    """
    proyectos = []
    if request.method == 'POST':
        form = BusquedaProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['columna'] == '1':
                """
                Si el patron a utilizar es el nombre
                """
                proyectos = Proyecto.objects.filter(
                    nombre=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '2':
                """
                Si el patron a utilizar es la fecha de inicio
                """
                proyectos = Proyecto.objects.filter(
                    fechaInicio=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de culminacion de un
                proyecto
                """
                proyectos = Proyecto.objects.filter(
                    fechaFinalizacion=form.cleaned_data['busqueda'])
    return render(request, 'administrarproyectos.html',
                  {'proyectos': proyectos,
                   'vacio': 'No se encuentran proyectos con ese '
                            'patron de busqueda',
                   'form': BusquedaProyectoForm()})


def administrarProyectosAsociados(request):
    usuario = Usuario.objects.all()
    id_user = request.user.id
    userSesion = User.objects.get(id=id_user)
    sesionado = userSesion.usuario
    proyectos = UsuariosXProyecto.objects.filter(usuario=sesionado, activo=True)
    permisos = request.session['permisos']
    c = []
    for u in proyectos:
        c.append(u.proyecto)
    return render(request, 'des_admin_proyectos.html',
                  {'proyectos': c,
                   'usuarios': usuario,
                   'permisos': permisos})


def administrarUsuariosAsociados(request, idProyect):
    proyecto = Proyecto.objects.get(id=idProyect)
    usu_proy = UsuariosXProyecto.objects.filter(proyecto=proyecto).exclude(lider=True)
    usuarios = []
    for u_p in usu_proy:
        usuarios.append(u_p.usuario)
    return render(request, 'AdministradorUsuarioProyecto.html', {'usuarios': usuarios,
                                                   'proyecto': proyecto,
                                                   'permisos': request.session['permisos']})


def asignarUsuarioProyecto(request, idProyect):
    """
    Vista que asigna los usuarios a un proyecto determinado.

    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo.

    @type idProyect: Unicode
    @param idProyect: Contiene el id del proyecto que se va a asociar/desasociar
    usuarios.

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    users = User.objects.exclude(id=1).exclude(id=request.user.id)
    usuarioXproy = UsuariosXProyecto.objects.filter(
                proyecto=Proyecto.objects.get(pk=idProyect)).exclude(
                lider=True)
    usr_proy = []
    for u in usuarioXproy:
        usr_proy.append(u.usuario)
    usuarios = []
    usuarios_aux = []
    for u in users:
        roles = u.usuario.roles.all()
        if roles:
            if roles.__len__() > 1:
                usuarios_aux.append(u.usuario)
            else:
                if roles[0].nombre != 'Lider':
                    usuarios_aux.append(u.usuario)
    for u in usuarios_aux:
        if u not in usr_proy:
            usuarios.append(u)
    if request.method == 'POST':
        usuariosProyect = request.POST.getlist('usuariosAsig')
        for u in usuariosProyect:
            usuario = Usuario.objects.get(id=u)
            try:
                UsuariosXProyecto.objects.create(
                        proyecto=proyecto,
                        usuario=usuario,
                        activo=True,
                        lider=False)
                proyecto.nroMiembros += 1
                proyecto.save()
                messages.success(request,
                                 'El usuario ' +
                                 usuario.user.username
                                 + ' ha sido asignado al proyecto ' +
                                 proyecto.nombre)
            except Exception:
                messages.error(request,
                               'Ha ocurrido un erro interno, favor'
                               ' contacte al administrador')
        return HttpResponseRedirect(reverse('sigma:adm_proy_usu', args=[idProyect]))
    else:
        pass
    return render(request, 'AsignarUsuario.html', {'usuarios': usuarios,
                                                   'proyecto': proyecto,
                                                   'permisos': request.session['permisos']})


def desasignarUsuarioProyecto(request, idProyect, idUser):
    usuario = Usuario.objects.get(id=idUser)
    proyecto = Proyecto.objects.get(id=idProyect)
    uxp = UsuariosXProyecto.objects.get(proyecto=proyecto, usuario=usuario)
    uxp.delete()
    messages.success(request, 'El usuario ' +
                              usuario.user.username
                              + ' ha sido desasignado del proyecto ' +
                              proyecto.nombre)
    return HttpResponseRedirect(reverse('sigma:adm_proy_usu', args=[idProyect]))


def asig_desagig_roles_proyecto(request, idProyect, idUser):
    proyecto = Proyecto.objects.get(id=idProyect)
    usuario = Usuario.objects.get(id=idUser)
    #roles = usuario.roles.all().exclude(nombre='Lider')
    rol_lider = Rol.objects.get(nombre='Lider')
    roles_usuario = UsuarioRol.objects.filter(usuario=usuario,
                               idProyecto=0,
                               idFase=0,
                               idItem=0).exclude(rol=rol_lider)
    roles = []
    for r_u in roles_usuario:
        roles.append(r_u.rol)
    rolXusuario = UsuarioRol.objects.filter(usuario=usuario, idProyecto=idProyect)
    rol_usr = roles[0]
    if rolXusuario:
        rol_usr = rolXusuario[0].rol
    if request.method == 'POST':
        idrol = request.POST['roles']
        rol = Rol.objects.get(id=idrol)
        if rolXusuario:
            if rol != rol_usr:
                UsuarioRol.objects.get(id=rolXusuario[0].id).delete()
                UsuarioRol.objects.create(usuario=usuario, rol=rol, idProyecto=idProyect)
                messages.success(request, 'El usuario ' +
                                      usuario.user.username
                                      + ' ahora posee el rol ' +
                                      rol.nombre)
                return HttpResponseRedirect(reverse('sigma:adm_proy_usu', args=[idProyect]))
            else:
                messages.info(request, 'El usuario no sufrio modificacion alguna')
                return HttpResponseRedirect(reverse('sigma:adm_proy_usu', args=[idProyect]))
        else:
            UsuarioRol.objects.create(usuario=usuario, rol=rol, idProyecto=idProyect)
            messages.success(request, 'El usuario ' +
                                  usuario.user.username
                                  + ' ahora posee el rol ' +
                                  rol.nombre)
        return HttpResponseRedirect(reverse('sigma:adm_proy_usu', args=[idProyect]))
    return render(request, 'UsuarioRolProyecto.html', {'proyecto': proyecto,
                                                       'usuario': usuario,
                                                       'roles': roles,
                                                       'rol_usr': rol_usr})




def iniciarProyecto(request, idProyect):
    """
    Vista que asigna los usuarios a un proyecto determinado.

    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo.

    @type idProyect: Unicode
    @param idProyect: Contiene el id del proyecto que se va a iniciar.

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    fases = Fase.objects.filter(proyecto=proyecto)
    comite = Comite.objects.get(proy=proyecto)
    usuComite = UsuarioPorComite.objects.filter(comite=comite)
    if fases.__len__() != proyecto.nroFases:
        messages.error(request, 'No puede iniciar el proyecto, aun no se han'
                                ' definido todas las fases')
        return HttpResponseRedirect(reverse('sigma:adm_proy'))
    if usuComite.__len__() < 3:
        messages.error(request, 'No puede iniciar el proyecto, aun no se han'
                                ' definido a todos los miembros del comite')
        return HttpResponseRedirect(reverse('sigma:adm_proy'))
    try:
        proyecto.estado = 'Iniciado'
        proyecto.fechaInicio = datetime.datetime.now()
        fase = fases.get(posicionFase=1)
        fase.estado = 'Iniciado'
        fase.save()
        proyecto.save()
        messages.success(request,
                         'El proyecto ' + proyecto.nombre + ' ha sido iniciado, '
                                                            'el lider ya puede '
                                                            'trabajar por el')
    except Exception:
        messages.error(request, 'Ha ocurrido un error interno')
        sys.exc_info()
    return HttpResponseRedirect(reverse('sigma:adm_proy'))