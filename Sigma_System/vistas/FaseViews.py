from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from Sigma_System.forms import BusquedaFasesForm
from Sigma_System.models import Proyecto, Usuario, Fase, TipoDeItem
import datetime, time


def administrar_fases(request, idProyect):
    """
    Vista para realizar la administracion de las fases de un proyecto
    @param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    request.session['idProyectoActual'] = idProyect
    proyecto = Proyecto.objects.get(pk=idProyect)
    fases = Fase.objects.filter(proyecto=proyecto).order_by('posicionFase')
    return render(request, 'administrarfases.html',
                  {'proyecto': proyecto, 'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases asociadas a este '
                            'proyecto'})


def alta_fase(request, idProyect):
    """
    Vista para realizar la alta de una fase
    @param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(pk=idProyect)
        nombre = request.POST['nombre']
        fase = Fase.objects.filter(proyecto=proyecto)
        for fas in fase:
            if fas.nombre == nombre:
                messages.error(request, 'Nombre de fase ya utilizado')
                return render(request, 'fasealta.html',
                              {'proyecto': idProyect})

        print fase.last().__getattribute__('nombre')

        if request.POST['fechaInicio'] > request.POST['fechaFin']:
            messages.error(request, 'La fecha de Inicio no puede ser'
                                    'superior a la fecha de fin')
            return render(request, 'fasealta.html',
                          {'proyecto': idProyect, 'fase': fase})
        print 3
        if fase.__len__() > 0:
            ultfase = fase.last()
            if ultfase is not None:
                print str(ultfase.__getattribute__('fechaFin'))
                if str(ultfase.__getattribute__('fechaFin')) > \
                        request.POST['fechaInicio']:
                    messages.error(request,
                                   'La fecha de Inicio de esta '
                                   'fase debe ser mayor a la fecha de  '
                                   'fin de la fase anterior')
                    return render(request, 'fasealta.html',
                                  {'fase': fase, 'proyecto': idProyect})
        faseNueva = Fase.objects.create(
            proyecto=proyecto,
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            posicionFase=Fase.objects.filter(
                proyecto=proyecto).__len__() + 1,
            estado='Pendiente',
            fechaInicio=request.POST['fechaInicio'],
            fechaFin=request.POST['fechaFin']
        )
        print faseNueva.fechaInicio.__class__

        proyecto.nroFases = Fase.objects.filter(proyecto=proyecto).__len__()
        proyecto.save()
        messages.success(request, 'Fase creada con exito')
        return HttpResponseRedirect(
            '/ss/proyecto/' + str(idProyect) + '/fase/')

    return render(request, 'fasealta.html', {'usuarios': usuarios,
                                             'proyecto': idProyect})


def modificar_fase(request, idProyect, idFase):
    """
    Vista para realizar la modificacion de datos de una fase
    :param idProyect: pk del proyecto sobre el cual se esta trabajando
    :param idFase: pk de la fase que se quiere modificar
    """
    fase = Fase.objects.get(pk=idFase)
    fase.fechaInicio = str(fase.fechaInicio)
    fase.fechaFin = str(fase.fechaFin)
    proyecto = Proyecto.objects.get(pk=idProyect)
    if request.method == 'POST':
        if fase.nombre == request.POST['nombre'] or Fase.objects.get(
                nombre=request.POST['nombre']):
            if fase.posicionFase > 1:
                faseAnt = Fase.objects.get(posicionFase=fase.posicionFase - 1)
                if str(faseAnt.fechaFin) > request.POST['fechaInicio']:
                    return render(request, 'fasemodificar.html',
                                  {'proyecto': idProyect, 'fase': fase,
                                   'alerta': 'La fecha de Inicio de esta fase '
                                             'es inferior a la fecha de '
                                             'fin de la fase anterior'})
            print proyecto.nroFases
            if fase.posicionFase < proyecto.nroFases:
                faseSig = Fase.objects.get(posicionFase=fase.posicionFase + 1)
                if str(faseSig.fechaInicio) < request.POST['fechaFin']:
                    messages.error(request, 'La fecha de fin de esta fase '
                                            'es superior a la fecha de '
                                            'inicio de la fase siguiente')
                    return render(request, 'fasemodificar.html',
                                  {'proyecto': idProyect, 'fase': fase})
            if request.POST['fechaInicio'] > request.POST['fechaFin']:
                messages.error(request, 'La fecha de Inicio se encuentra '
                                        'mas adelantada que la fecha de fin')
                return render(request, 'fasemodificar.html',
                              {'proyecto': idProyect, 'fase': fase})

            fases = Fase.objects.filter(proyecto=proyecto).exclude(pk=idFase)
            for fas in fases:
                if fas.nombre == request.POST['nombre']:
                    messages.error(request, 'Nombre ya existe en el sistema')
                    return render(request, 'fasemodificar.html',
                                  {'proyecto': idProyect, 'fase': fase})

            fase.nombre = request.POST['nombre']
            fase.descripcion = request.POST['descripcion']
            fase.fechaInicio = request.POST['fechaInicio']
            fase.fechaFin = request.POST['fechaFin']
            fase.save()
            proyecto.fechaInicio = Fase.objects.get(
                proyecto=proyecto,
                posicionFase=1).fechaInicio
            proyecto.fechaFinalizacion = Fase.objects.get(
                proyecto=proyecto,
                posicionFase=proyecto.nroFases).fechaFin
            proyecto.save()
            messages.success(request, 'Fase modificada con exito')
            return HttpResponseRedirect(
                '/ss/proyecto/' + str(idProyect) + '/fase/')
    return render(request, 'fasemodificar.html', {'proyecto': idProyect,
                                                  'fase': fase})


def baja_fase(request, idProyect, idFase):
    """
    Vista para realizar la baja de una fase
    @param request: contiene los datos de la pagina que lo llamo.
    @param idProyect: pk del proyecto sobre el cual se esta trabajando.
    @param idFase: pk de la fase que se quiere dar de baja.

    @return: Administrarfase.html
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyect)
        fase = Fase.objects.get(pk=idFase)
        if fase.estado != 'Pendiente':
            return render(request, 'fasebaja.html',
                          {'alerta': 'No se puede suprimir la fase: '
                                     'se encuentra activa',
                           'proyecto': idProyect})
        elif TipoDeItem.objects.filter(fase=fase).__len__() > 0:
            return render(request, 'fasebaja.html',
                          {'alerta': 'No se puede suprimir la fase: '
                                     'contiene Tipos de Items Asociados.',
                           'proyecto': idProyect})
        else:
            fase.delete()
            fases = Fase.objects.filter(proyecto=proyecto).order_by(
                'posicionFase')
            posicion = 1
            for fas in fases:
                fas.posicionFase == posicion
                fas.save()
                posicion += 1
            proyecto.nroFases = posicion - 1
            proyecto.save()
        print 'Hola'
    return HttpResponseRedirect('/ss/proyecto/' + str(idProyect) + '/fase/')


def buscar_fase(request, idProyect):
    """
    Vista para realizar la busqueda de fases
    :param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    fases = []
    if request.method == 'POST':
        form = BusquedaFasesForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['columna'] == '1':
                """
                Si el patron a utilizar es el nombre
                """
                fases = Fase.objects.filter(
                    nombre=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '2':
                """
                Si el patron a utilizar es el estado de la fase
                """
                fases = Fase.objects.filter(
                    estado=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de inicio de la fase
                """
                fases = Fase.objects.filter(
                    fechaInicio=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de fin de la fase
                """
                fases = Fase.objects.filter(
                    fechaFin=form.cleaned_data['busqueda'])
    return render(request, 'administrarfases.html',
                  {'proyecto': Proyecto.objects.get(pk=idProyect),
                   'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases que coincidan '
                            'con el patron de busqueda'})


def intercambiarFase(request, idProyect):
    pass