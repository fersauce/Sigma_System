from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from Sigma_System.forms import BusquedaProyectoForm, AltaProyectoForm
from Sigma_System.models import Proyecto, Usuario, Fase
import datetime


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
    """
    if request.method == 'POST':
        form = AltaProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = Proyecto.objects.filter(
                nombre=form.cleaned_data['nombreProyecto'])
            if proyecto.__len__() == 0:
                fecha = datetime.datetime.now()
                fecha2 = fecha + datetime.timedelta(
                    days=form.cleaned_data['duracion'])
                print str(fecha) + '\n' + str(fecha2)
                nuevoProyecto = Proyecto.objects.create(
                    nombre=form.cleaned_data['nombreProyecto'],
                    fechaCreacion=fecha,
                    descripcion=form.cleaned_data['descripcion'],
                    duracion=form.cleaned_data['duracion'],
                    complejidad=0,
                    costo=0,
                    estado='Pendiente',
                    nroFases=0,
                    nroMiembros=0,
                    fechaInicio=fecha,
                    fechaFinalizacion=fecha2)
                print Usuario.objects.get(user=User.objects.get(
                    username=form.cleaned_data['lider'])).__str__()
                print str(form.cleaned_data['duracion'])
                print str(form.cleaned_data['lider'])
                return HttpResponseRedirect('/ss/proyecto/')
            else:
                form = AltaProyectoForm()
                return render(request, 'proyectoalta.html',
                              {'form': form,
                               'alerta': 'Proyecto ya existente '
                                         'con ese nombre'})
    else:
        print '3'
        form = AltaProyectoForm()
    return render_to_response('proyectoalta.html', {'form': form},
                              context_instance=RequestContext(request))


def modificar_proyecto(request, idProyecto):
    """
    Vista para realizar la modificacion de datos del proyecto
    """
    proyecto = Proyecto.objects.get(pk=idProyecto)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        if proyecto.estado == 'Iniciado':
            proyecto.duracion = request.POST['duracion']
        else:
            proyecto.nombre = request.POST['nombre']
            proyecto.descripcion = request.POST['descripcion']
            proyecto.duracion = request.POST['duracion']
            proyecto.fechaFinalizacion = proyecto.fechaInicio + \
                                         datetime.timedelta(
                                             days=int(proyecto.duracion))
            print str(proyecto.fechaFinalizacion) + 'hola' + str(
                datetime.timedelta(days=int(proyecto.duracion)))
        proyecto.save()
        return HttpResponseRedirect('/ss/proyecto')
    return render(request, 'proyectomodificar.html', {'proyecto': proyecto,
                                                      'choices': usuarios})


def baja_proyecto(request, idProyecto):
    """
    Vista para realizar la baja de un proyecto.
    :param idProyecto: pk del proyecto a ser suprimido del sistema.
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyecto)
        if proyecto.estado == 'Iniciado':
            return render(request, 'proyectobaja.html', {
                'alerta': 'No se puede suprimir el proyecto'})
        elif Fase.objects.filter(proyecto=proyecto).__len__() > 0:
            return render(request, 'proyectobaja.html', {
                'alerta': 'No se puede suprimir el proyecto'})
        else:
            proyecto.delete()
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


