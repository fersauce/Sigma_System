from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render
from django.http import *
import simplejson
import sys
from Sigma_System.forms import BusquedaFasesForm
from Sigma_System.models import Proyecto, Usuario, Fase, TipoDeItem, LBase, \
    Items_x_LBase, Item, Solicitud
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
        if fases and proyecto.estado != "Iniciado":
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
        if fase.nombre == request.POST['nombre'] or Fase.objects.get(
                nombre=request.POST['nombre']):
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


def linea_base(request, idProyecto, idFase):
    lb = LBase.objects.filter(fase=Fase.objects.get(id=idFase)).order_by('id')
    return render(request, 'LineaBase.html',
                  {'id_proy': idProyecto, 'id_fase': idFase, 'lineasbase': lb})


def establecer_linea_base(request, idProyecto, idFase):
    itemfinales = traer_itemfinales(idFase)
    if request.method == 'POST':
        obs = request.POST['obs']
        lb = LBase.objects.create(obs=obs, fase=Fase.objects.get(id=idFase))
        i_finales = request.POST.getlist('items_finales')
        for i in i_finales:
            item_actual = Item.objects.get(id=i)
            item_actual.estado = 'bloqueado'
            item_actual.save()
            Items_x_LBase.objects.create(lb=lb, item=item_actual,
                                         item_final=True)
        i_padres = traer_items_padre(i_finales, idFase)
        for i in i_padres:
            i.estado = 'bloqueado'
            i.save()
            Items_x_LBase.objects.create(lb=lb, item=i)
        fase = Fase.objects.get(pk=idFase)
        proyecto = fase.proyecto
        if not proyecto.nroFases == fase.posicionFase:
            faseSig = Fase.objects.get(posicionFase=fase.posicionFase + 1,
                                       proyecto=proyecto)
            if faseSig.estado == 'Pendiente':
                faseSig.estado = 'Iniciado'
                fase.fechaInicio = datetime.datetime.now()
                faseSig.save()
                messages.success(request, 'Fase ' + fase.nombre + ' iniciada.')
        messages.success(request,
                         'Se agregaron correctamente los items a la linea base')
        return HttpResponseRedirect(
            reverse('sigma:adm_fase_lb', args=(idProyecto, idFase)))
    else:
        return render(request, 'AsignarItemxLB.html',
                      {'id_proy': idProyecto, 'id_fase': idFase,
                       'itemfinales': itemfinales})


def traer_itemfinales(idFase):
    fase = Fase.objects.get(id=idFase)
    items = Item.objects.filter(tipoItems__fase=fase, estado='aprobado')
    items_finales = []
    for i in items:
        i_hijo = Item.objects.filter(item_padre=i.id, tipoItems__fase=fase)
        if not i_hijo:
            items_finales.append(i)
    return items_finales


def traer_items_padre(i_finales, idFase):
    fase = Fase.objects.get(id=idFase)
    items_padre = []
    for i in i_finales:
        i_actual = Item.objects.get(id=i)
        while i_actual.item_padre != 0 and i_actual.tipoItems.fase == fase:
            i_actual = Item.objects.get(id=i_actual.item_padre)
            if i_actual not in items_padre:
                items_padre.append(i_actual)
    return items_padre


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
                # Si el patron a utilizar es la fecha de fin de la fase
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


def finalizar_fase(request, idp, idf):
    fase = Fase.objects.get(id=idf)
    anteriores = Fase.objects.filter(posicionFase__lt=fase.posicionFase)
    for ante in anteriores:
        if ante.estado != 'Cerrado':
            messages.error(request, 'No se puede finalizar la fase, aun '
                                    'hay fases anteriores sin finalizar, '
                                    'finalicelas y luego vuelva '
                                    'a intentarlo')
            return HttpResponseRedirect(reverse('sigma:adm_fase', args=[idp]))
    items = Item.objects.get(tipoItems__fase=fase)
    for item in items:
        if item.estado != 'Bloqueado':
            messages.error(request, 'No se puede finalizar la fase, aun '
                                    'hay fases items flotantes, '
                                    'verifiquelos y luego vuelva '
                                    'a intentarlo')
            return HttpResponseRedirect(reverse('sigma:adm_fase', args=[idp]))
    solicitudes = Solicitud.objects.filter(fase=fase, activo=True)
    for solicitud in solicitudes:
        if solicitud.estado in ['Pendiente', 'Votacion', 'Aprobado',
                                'Ejecucion']:
            messages.error(request, 'No se puede finalizar la fase, aun '
                                    'hay solicitudes sin finalizar, '
                                    'verifiquelos y luego vuelva '
                                    'a intentarlo')
            return HttpResponseRedirect(reverse('sigma:adm_fase', args=[idp]))
    try:
        with transaction.atomic():
            fase.estado = 'Cerrado'
            fase.fechaFin = datetime.datetime.now()
            fase.save()
            messages.success(request,
                             'Se ha finalizado correctamente la fase "' + fase.nombre + '"')
    except Exception:
        print sys.exc_info()
        messages.error(request,
                       'Ocurrio un error al intentar finalizar la fase')
    proyecto = Proyecto.objects.get(pk=idp)
    if fase.posicionFase < proyecto.nroFases:
        faseSiguiente = fase.objects.filter(proyecto=proyecto).get(
            posicionFase=fase.posicionFase + 1)
        if faseSiguiente.estado == 'Pendiente':
            try:
                with transaction.atomic():
                    faseSiguiente.estado = 'Iniciado'
                    faseSiguiente.fechaInicio = fase.fechaFin
                    fase.save()
                    messages.success(request,
                                     'Se ha iniciado correctamente la fase "' +
                                     faseSiguiente.nombre + '"')
            except Exception:
                print sys.exc_info()
                messages.error(request,
                               'Ocurrio un error al intentar iniciar la fase.')
    else:
        proyecto.estado = 'Culminado'
        proyecto.fechaFinalizacion = fase.fechaFin
        proyecto.save()
    return HttpResponseRedirect(reverse('sigma:adm_fase', args=[idp]))