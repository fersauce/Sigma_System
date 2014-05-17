from django.contrib import messages
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.serializers import serialize
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
import simplejson
import sys
from Sigma_System.forms import BusquedaProyectoForm, AltaProyectoForm
from Sigma_System.models import Proyecto, Usuario, Fase, UsuariosXProyecto, \
    UsuarioRol, Rol, Comite, UsuarioPorComite
import datetime, time


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
    proyectos = Proyecto.objects.all().order_by('-nombre')
    usuario = Usuario.objects.all()
    return render(request, 'administrarproyectos.html',
                  {'proyectos': proyectos,
                   'usuarios': usuario,
                   'form': BusquedaProyectoForm()})


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
    rol = Rol.objects.get(pk=5)
    lideres = UsuarioRol.objects.filter(rol__pk=rol.pk)
    if request.method == 'POST':
        proyecto = Proyecto.objects.filter(
            nombre=request.POST['nombreProyecto'])
        if proyecto.__len__() == 0:
            fecha = datetime.datetime.now()
            try:
                tl = Usuario.objects.get(pk=request.POST['lider'])
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
                        days=10),
                    lider=tl
                )
                nuevoProyecto.save()
                lider = UsuariosXProyecto(
                    proyecto=nuevoProyecto,
                    usuario=tl,
                    activo=True,
                    lider=True
                )
                lider.save()
                usuarios = Usuario.objects.all().exclude(pk=tl.pk)
                for usuario in usuarios:
                    UsuariosXProyecto.objects.create(
                        proyecto=nuevoProyecto,
                        usuario=usuario
                    )
                comite = Comite.objects.create(
                    obs='Comite de cambios del proyecto ' +
                        nuevoProyecto.nombre + '',
                    nro_integ=1,
                    fecha_creacion=datetime.datetime.now(),
                    proy=nuevoProyecto
                )
                usuariosComite = UsuarioPorComite.objects.create(
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
    return HttpResponseRedirect('/ss/proyecto/')


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
    proyectos = Proyecto.objects.all()
    c = {}
    c.update(csrf(request))
    return render(request, 'des_admin_proyectos.html',
                  {'proyectos': proyectos, 'usuarios': usuario})


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
    if request.is_ajax():
        print 'LLamada de ajax'
        enviar = []
        for u in UsuariosXProyecto.objects.filter(
                proyecto=Proyecto.objects.get(pk=idProyect)).exclude(
                lider=True):
            enviar.append(
                {'id': u.usuario.pk, 'nombre': u.usuario.user.first_name,
                 'apellido': u.usuario.user.last_name, 'activo': u.activo})
        return HttpResponse(simplejson.dumps(enviar),
                            mimetype='application/json')
    usuariosProyect = request.GET.getlist('usuarioAsig')
    proyecto = Proyecto.objects.get(pk=idProyect)
    usuarios = UsuariosXProyecto.objects.filter(proyecto=proyecto).exclude(
        lider=True)
    bandera = False
    for u in usuarios:
        if str(u.usuario.pk) in usuariosProyect:
            if not u.activo:
                try:
                    u.activo = True
                    u.save()
                    proyecto.nroMiembros += 1
                    proyecto.save()
                    messages.success(request,
                                     'El usuario ' +
                                     u.usuario.user.first_name
                                     + ' ha sido asignado al proyecto ' +
                                     proyecto.nombre)
                    bandera = True
                except Exception:
                    messages.error(request, 'Ha ocurrido un erro interno, favor'
                                            ' contacte al administrador')
        else:
            if u.activo:
                try:
                    u.activo = False
                    u.save()
                    proyecto.nroMiembros -= 1
                    proyecto.save()
                    messages.success(request,
                                     'El usuario ' +
                                     u.usuario.user.first_name
                                     + ' ha sido desasignado del proyecto ' +
                                     proyecto.nombre)
                    bandera = True
                except Exception:
                    messages.error(request, 'Ha ocurrido un error interno,'
                                            'favor contacte al administrador')
    if not bandera:
        messages.info(request, 'No se han realizados asignaciones/'
                               'desasignaciones en el proyecto ' +
                               proyecto.nombre)
    return HttpResponseRedirect(reverse('sigma:adm_proy'))


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
    if fases.__len__() != proyecto.nroFases:
        messages.error(request, 'No puede iniciar el proyecto, aun no se han'
                                ' definido todas las fases')
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