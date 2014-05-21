from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import *
import simplejson
from Sigma_System.forms import BusquedaFasesForm
from Sigma_System.models import Proyecto, Usuario, Fase, TipoDeItem
from Sigma_System.decoradores import permisos_requeridos
from django.contrib.auth.decorators import login_required
import datetime, time


@login_required(login_url='/login/')
def administrar_fases(request, idProyect):
    """
    Vista para acceder a la administracion de fases de un proyecto.
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: codigo del proyecto del cual se van a trabajar.
    """
    request.session['idProyectoActual'] = idProyect
    proyecto = Proyecto.objects.get(pk=idProyect)
    fases = Fase.objects.filter(proyecto=proyecto).order_by('posicionFase')
    permisos = request.session['permisos']
    return render(request, 'administrarfases.html',
                  {'proyecto': proyecto, 'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases asociadas a este '
                            'proyecto',
                   'permisos': permisos})


@login_required(login_url='/login/')
@permisos_requeridos(['crear_fa'], 'sigma:adm_fase', 'crear fases', 1)
def alta_fase(request, idProyect):
    """
    Vista para realizar la alta de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: codigo del proyecto del cual se van a trabajar.
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
        Fase.objects.create(
            proyecto=proyecto,
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            posicionFase=Fase.objects.filter(
                proyecto=proyecto).__len__() + 1,
            estado='Pendiente',
            fechaInicio=datetime.datetime.now(),
            fechaFin=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        fases = Fase.objects.filter(proyecto=proyecto)
        if fases.__len__() == 1:
            proyecto.estado = "Iniciado"
        proyecto.save()
        messages.success(request, 'Fase creada con exito')
        return HttpResponseRedirect(
            '/ss/proyecto/' + str(idProyect) + '/fase/')
    else:
        proyecto = Proyecto.objects.get(pk=idProyect)
        fases = Fase.objects.filter(proyecto=proyecto)
        if fases.__len__() == proyecto.nroFases:
            messages.error(request,
                           'Ya no puede agregar mas fases, ya se encuentran '
                           'todas las fases creadas.')
            return HttpResponseRedirect(
                reverse('sigma:adm_fase', args=[idProyect]))
    return render(request, 'fasealta.html', {'usuarios': usuarios,
                                             'proyecto': idProyect})


@login_required(login_url='/login/')
@permisos_requeridos(['modificar_fa'], 'sigma:adm_fase', 'modificar fases', 1)
def modificar_fase(request, idProyect, idFase):
    """
    Vista para realizar la modificacion de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.
    @type idProyect: Unicode
    @param idProyect: pk del proyecto sobre el cual se esta trabajando.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere modificar.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    fase = Fase.objects.get(pk=idFase)
    proyecto = Proyecto.objects.get(pk=idProyect)
    if request.method == 'POST':
        if fase.nombre == request.POST['nombre'] or Fase.objects.get(nombre=request.POST['nombre']):
            print proyecto.nroFases
            fases = Fase.objects.filter(proyecto=proyecto).exclude(pk=idFase)
            fase.nombre = request.POST['nombre']
            fase.descripcion = request.POST['descripcion']
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
                reverse('sigma:adm_fase', args=[idProyect]))
    return render(request, 'fasemodificar.html', {'proyecto': idProyect,
                                                  'fase': fase})


@login_required(login_url='/login/')
@permisos_requeridos(['eliminar_fa'], 'sigma:adm_fase', 'eliminar fases', 1)
def baja_fase(request, idProyect, idFase):
    """
    Vista para realizar la baja de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: pk del proyecto sobre el cual se esta trabajando.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere dar de baja.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyect)
        fase = Fase.objects.get(pk=idFase)
        if fase.estado != 'Pendiente':
            messages.error(request,
                           'No se puede suprimir la fase: se encuentra activa')
            return render(request, 'fasebaja.html',
                          {'proyecto': idProyect})
        elif TipoDeItem.objects.filter(fase=fase).__len__() > 0:
            messages.error(request,
                           'No se puede suprimir la fase: contiene Tipos de '
                           'Items Asociados.')
            return render(request, 'fasebaja.html',
                          {'proyecto': idProyect})
        else:
            try:
                fase.delete()
                fases = Fase.objects.filter(proyecto=proyecto).order_by(
                    'posicionFase')
                posicion = 1
                for fas in fases:
                    fas.posicionFase == posicion
                    fas.save()
                    posicion += 1
            except Exception:
                messages.error(request, 'Ha ocurrido un error interno')
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
                #Si el patron a utilizar es la fecha de fin de la fase
                fases = Fase.objects.filter(
                    fechaFin=form.cleaned_data['busqueda'])
    return render(request, 'administrarfases.html',
                  {'proyecto': Proyecto.objects.get(pk=idProyect),
                   'fases': fases,
                   'form': BusquedaFasesForm()})


def intercambiarFase(request, idFase):
    """
    Vista que realiza el intercambio de fases (Esto lo puede realizar solo en
    tiempo de creacion, una vez iniciado el proyecto, esto ya no puede variar)

    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere cambiar.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    fase = Fase.objects.get(pk=idFase)
    if request.is_ajax():
        print "Llamada Ajax de intercambiarFase"
        try:
            enviar = []
            for u in Fase.objects.filter(proyecto=fase.proyecto,
                                         estado='Pendiente').exclude(
                    pk=idFase).order_by('posicionFase'):
                enviar.append({'pkFase': u.pk, 'posicion': u.posicionFase,
                               'nombre': u.nombre})
            return HttpResponse(simplejson.dumps(enviar),
                                mimetype='application/json')
        except DeprecationWarning:
            print "Solo es warning"
    opcion = request.GET['posicion']
    faseIntercambiada = Fase.objects.get(pk=opcion)
    try:
        pasador = fase.posicionFase
        fase.posicionFase = faseIntercambiada.posicionFase
        faseIntercambiada.posicionFase = pasador
        fase.save()
        faseIntercambiada.save()
        messages.success(request,
                         'se han intercambiado satisfactoriamente la fase ' +
                         fase.nombre + ' con la fase ' + faseIntercambiada.nombre)
    except Exception:
        messages.error(request, 'Solo es precaucion')
    return HttpResponseRedirect(
        reverse('sigma:adm_fase', args=[fase.proyecto.pk]))