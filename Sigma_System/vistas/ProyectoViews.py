from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from Sigma_System.forms import BusquedaProyectoForm, AltaProyectoForm
from Sigma_System.models import Proyecto, Usuario, Fase
import datetime, time


def administrar_proyecto(request):
    """
    Vista para acceder a la administracion de proyectos.
    """
    proyectos = Proyecto.objects.all().order_by('-nombre')
    return render(request, 'administrarproyectos.html',
                  {'proyectos': proyectos,
                   'vacio': 'No se encuentran proyectos registrados',
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
    if request.method == 'POST':
        proyecto = Proyecto.objects.filter(
            nombre=request.POST['nombreProyecto'])
        if proyecto.__len__() == 0:
            fecha = datetime.datetime.now()
            try:
                print request.POST['fechaInicio']
                nuevoProyecto = Proyecto(
                    nombre=request.POST['nombreProyecto'],
                    fechaCreacion=fecha,
                    descripcion=request.POST['descripcion'],
                    complejidad=0,
                    costo=0,
                    estado='Pendiente',
                    nroFases=0,
                    nroMiembros=1,
                    duracion=0,
                    fechaInicio=datetime.datetime.now(),
                    fechaFinalizacion=datetime.datetime.now() + datetime.timedelta(
                        days=10)
                )
                nuevoProyecto.save()
                messages.success(request, 'Proyecto ' + str(
                    nuevoProyecto.nombre) + ' creado con exito')
            except Exception as error:
                messages.error(request, 'Ocurrio un error al crear el '
                                        'proyecto')
                print error.args
            return HttpResponseRedirect('/ss/proyecto/')
        else:
            messages.error(request,
                           'No se pudo crear el proyecto: El nombre ya '
                           'existe en el sistema.')
            return render(request, 'proyectoalta.html')

    return render_to_response('proyectoalta.html',
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
