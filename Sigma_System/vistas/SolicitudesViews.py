import datetime
import traceback
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import simplejson
import sys
from Sigma_System.models import Usuario, UsuariosXProyecto, Solicitud, Proyecto, \
    LBase, Items_x_LBase, Item, Archivo, Fase, HistorialLineabase
from Sigma_System.views import inicio


def administrarProyectosSolicitudes(request):
    """
    :param request: Contiene informacion de la pagina que solicito la vista
    :type request: django.http.HttpRequest
    :return: vista que presenta las solicitudes realizadas por el usuario.
    :rtype: None
    """
    id_user = request.user.id
    print id_user
    try:
        userSesion = User.objects.get(id=id_user)
        sesionado = userSesion.usuario
        proyectos = UsuariosXProyecto.objects.filter(usuario=sesionado,
                                                     activo=True)
        permisos = request.session['permisos']
        solicitudes = Solicitud.objects.filter(id_usuario=id_user).exclude(
            activo=False)
        c = []
        """for u in proyectos:
            c.append(
                {'proyecto': u.proyecto, 'nroSol': Solicitud.objects.filter(
                    proyecto=u.proyecto.pk, activo=True).__len__()})"""
        return render(request, 'solicitudes_proyectos.html',
                      {'solicitudes': solicitudes, 'permisos': permisos})
    except Exception:
        print traceback.print_exc()
        messages.error(request, 'Fallo en el servidor')
        return inicio(request)


def administrarSolicitudes(request, idFase):
    fase = Fase.objects.get(pk=idFase)
    solicitudes = Solicitud.objects.filter(fase=fase,
                                           id_usuario=Usuario.objects.get(
                                               user=request.user).pk).exclude(
        activo=False)
    return render(request, 'solicitudes_listado.html',
                  {'proyecto': fase.proyecto, 'fase': fase,
                   'solicitudes': solicitudes})


def administrarSolicitudesProyectoFase(request, idProyecto):
    proyecto = Proyecto.objects.get(pk=idProyecto)
    fases = Fase.objects.filter(proyecto=proyecto)
    return render(request, 'solicitudes_fases.html',
                  {'proyecto': proyecto, 'fases': fases})


def altaSolicitud(request):
    """
    Controlador que se encargar de realizar el alta correspondiente de la
    solicitud que se ha encar
    :param request: Contiene informacion de la pagina que solicito la vista
    :type request: django.http.HttpRequest
    :return: almacenamiento de la nueva solicitud
    :rtype: None
    """
    if request.method == 'POST':
        idProyecto = request.POST['idProyecto']
        idFase = request.POST['idFase']
        if not request.POST.getlist('itemSeleccionado'):
            messages.info(request, 'No se ha seleccionado ningun item, '
                                   'por ello la solicitud no se ha creado')
        else:
            try:
                with transaction.atomic():
                    fase = Fase.objects.get(pk=idFase)
                    solicitud = Solicitud.objects.create(
                        codigo='P' + str(fase.proyecto.pk) +
                               '-F' + str(fase.pk) +
                               '-S' + str(
                            Solicitud.objects.all().__len__() + 1),
                        justificacion=request.POST['justificacion'],
                        fecha_redaccion=datetime.datetime.now(),
                        fecha_respuesta=datetime.datetime.now(),
                        fecha_limite=datetime.datetime.now(),
                        impacto=0,
                        nro_votos_neg=0,
                        nro_votos_posit=0,
                        id_usuario=Usuario.objects.get(user=request.user).pk,
                        proyecto=fase.proyecto,
                        fase=fase,
                        activo=True
                    )
                    for i in request.POST.getlist('itemSeleccionado'):
                        item = Item.objects.get(pk=i)
                        solicitud.item.add(item)
                        item.estado = 'revision'
                        item.save()
                        hijos = Item.objects.filter(item_padre=item.pk)
                        for hijo in hijos:
                            hijo.estado = 'revision'
                            hijo.save()
                        solicitud.impacto += calcularImpacto(item)
                        lbs = Items_x_LBase.objects.filter(item=item,
                                                           lb__estado='cerrado')
                        for lb in lbs:
                            if not lb.lb in solicitud.lb_relacionadas.all():
                                solicitud.lb_relacionadas.add(lb.lb)
                                lb.lb.estado = 'comprometida'
                                print 'posible'
                                lb.lb.save()
                                HistorialLineabase.objects.create(
                                    id_usuario=solicitud.id_usuario,
                                    tipo_operacion=lb.lb.estado,
                                    id_solicitud=solicitud.pk,
                                    linea_base=lb.lb
                                )
                    solicitud.save()
                messages.success(request,
                                 'La solicitud se ha creado satisfactoriamente')
            except RuntimeError:
                print 'Solo warning'
                pass
            except Exception:
                print sys.exc_info()
                messages.error(request,
                               'Ha ocurrido un error al crear la solicitud')
    return administrarProyectosSolicitudes(request)


def bajaSolicitud(request, idSolicitud):
    solicitud = Solicitud.objects.get(pk=idSolicitud)
    if solicitud.estado != 'Pendiente':
        messages.info(request,
                      'No se puede suprimir la solicitud, ya '
                      'se encuentra en estado' + solicitud.estado)
        return render(request,
                      reverse('sigma:solic_adm', args=[solicitud.fase.pk]))
    try:
        with transaction.atomic():
            for item in solicitud.item.all():
                for hijo in Item.objects.filter(item_padre=item.pk):
                    hijo.estado = 'bloqueado'
                    hijo.save()
                item.estado = 'bloqueado'
                item.save()
            for lb in solicitud.lb_relacionadas.all():
                lb.estado = 'cerrado'
                lb.save()
                historial = HistorialLineabase.objects.create(
                    id_usuario=solicitud.id_usuario,
                    tipo_operacion=lb.estado,
                    id_solicitud=solicitud.pk,
                    linea_base=lb
                )
            solicitud.activo = False
            solicitud.save()
        messages.success(request, 'La solicitud ha sido eliminada')
    except Exception:
        print sys.exc_info()
        messages.error(request, 'Ha ocurrido un error al eliminar la solicitud')
    return administrarProyectosSolicitudes(request)


def enviarSolicitud(request, idSolicitud):
    """

    :param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo
    :type request: django.http.HttpRequest
    :param idSolicitud: id de la solicitud a ser enviada
    :type idSolicitud: int
    :return: Pagina para administrar las solicitudes hechas
    :rtype: django.http.response.HttpResponseRedirect
    """
    solicitud = Solicitud.objects.get(pk=idSolicitud)
    solicitud.estado = 'Votacion'
    solicitud.save()
    messages.success(request, 'La solicitud ha sido enviada para la votacion')
    return administrarProyectosSolicitudes(request)


def ejecutarSolicitud(request, idSolicitud):
    """
    Controlador que se encarga de habilitar la ejecucion de la solicitud pasada
    como parametro.
    :param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo
    :type request: django.http.HttpRequest
    :param idSolicitud: id de la solicitud a ser enviada
    :type idSolicitud: int
    :return: Pagina en donde se encuentra actualizado.
    """
    solicitud = Solicitud.objects.get(pk=idSolicitud)

    if solicitud.estado == 'Pendiente':
        messages.info(request, 'La solicitud ' + str(solicitud.codigo) +
                      ' no puede ser ejecutada hasta que no sea aprobada.')
    elif solicitud.estado == 'Votacion':
        messages.info(request, 'La solicitud ' + str(solicitud.codigo) +
                      ' no puede ser ejecutada porque se encuentra en proceso '
                      'de votacion.')
    elif solicitud.estado == 'Rechazado':
        messages.info(request, 'La solicitud ' + str(solicitud.codigo) +
                      ' ha sido rechazada y no puede ser ejecutada.')
    elif solicitud.estado == 'Ejecucion':
        messages.info(request, 'La solicitud ' + str(solicitud.codigo) +
                      ' esta siendo ejecutada.')
    elif solicitud.estado == 'Ejecutado':
        messages.info(request, 'La solicitud ' + str(solicitud.codigo) +
                      ' ya ha sido ejecutada.')
    else:
        try:
            with transaction.atomic():
                for item in solicitud.item.all():
                    item.estado = 'revision-desbloq'
                    item.save()
                    hijos = Item.objects.filter(item_padre=item.pk)
                    for hijo in hijos:
                        hijo.estado = 'revision-bloq'
                        hijo.save()
                for lb in solicitud.lb_relacionadas.all():
                    lb.estado = 'rota'
                    lb.save()
                    HistorialLineabase.objects.create(
                        id_usuario=solicitud.id_usuario,
                        tipo_operacion=lb.estado,
                        id_solicitud=idSolicitud,
                        linea_base=lb
                    )
                solicitud.estado = 'Ejecucion'
                solicitud.save()
            messages.success(request, 'La solicitud ha sido iniciada, ya puede'
                                      ' ejecutar los cambios sobre los items'
                                      ' de la solicitud')
        except Exception:
            print sys.exc_info()
            messages.error(request,
                           'Ocurrio un error al intentar ejecutar '
                           'la solicitud.')
    return administrarProyectosSolicitudes(request)


def recuperarItems(request, tipoTrans):
    """
    Vista que se encarga de recuperar los proyectos y fases asociadas al
    usuario logueado y tambien los items que se encuentran en lb para
    ingresarlos en una solicitud.

    :param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo
    :type request: django.http.HttpRequest
    :param idFase: Codigo de la fase asociada a la solicitud
    :type idFase: integer
    :return: Items que cumplen las condiciones ordenados por fase
    :rtype: lista
    """
    if request.is_ajax():

        if tipoTrans == '1':
            """
            Retorna los proyectos que tiene asociado el usuario.
            """
            idUsuario = request.user.id
            proyectos = UsuariosXProyecto.objects.filter(usuario=idUsuario)
            projects = []
            b = False
            print 'Hola'
            for proyecto in proyectos:
                if proyecto.proyecto.estado == 'Iniciado':
                    projects.append({'id_proy': proyecto.proyecto.pk,
                                     'nombre_proy': proyecto.proyecto.nombre})
                    b = True
            if not projects or not b:
                messages.error(request,
                               'No tiene proyectos asociados que se encuentran '
                               'en estado iniciado y/o han finalizado todos sus'
                               ' proyectos asociados')
                return HttpResponse(simplejson.dumps(''),
                                    content_type='applicationl/json')
            print projects
            return HttpResponse(simplejson.dumps(projects),
                                content_type='application/json')
        elif tipoTrans == '2':
            """
            Retorna las fases asociadas al usuario del proyecto seleccionado
            """
            idProyecto = request.GET['proyectoSeleccionado']
            proyecto = Proyecto.objects.get(id=idProyecto)
            fases = Fase.objects.filter(proyecto=proyecto)
            fasEnvio = []
            for fas in fases:
                fasEnvio.append({'pk_fase': fas.pk, 'nombre_fase': fas.nombre})
            return HttpResponse(simplejson.dumps(fasEnvio),
                                content_type='application/json')
            pass

        elif tipoTrans == '3':
            """
            Retorna la solicitud pedida
            """
            solicitud = Solicitud.objects.get(pk=request.GET['idSol'])
            c = []
            for i in solicitud.item.all():
                c.append({'item': i.nombre})
            return HttpResponse(simplejson.dumps(c),
                                content_type="application/json")
        else:
            idFase = request.GET['faseSeleccionada']
            fase = Fase.objects.get(pk=idFase)
            if fase.estado == 'Finalizado':
                return HttpResponse(simplejson.dumps([]),
                                    content_type='application/json')
            try:
                lbs = LBase.objects.filter(fase=fase)
                c = []
                for lb in lbs:
                    item_x_lb = Items_x_LBase.objects.filter(lb=lb).order_by(
                        'lb__fase')
                    for item in item_x_lb:
                        if not itemsParaSolicitud(item.item.pk):
                            c.append({
                                'item': {'pk_id': item.item.pk,
                                         'nombre': item.item.nombre},
                                'lb': {'pk_id': lb.pk, 'nombre': lb.obs},
                                'fase': {'pk': lb.fase.pk,
                                         'nombre': lb.fase.nombre}})
                c.sort()
                if not c:
                    return HttpResponse(simplejson.dumps(''),
                                        content_type='application/json')
                return HttpResponse(simplejson.dumps(c),
                                    content_type='application/json')
            except Exception:
                print sys.exc_info()
                return administrarProyectosSolicitudes(request)


def familiaItems(request):
    if request.is_ajax():
        try:
            item = Item.objects.get(pk=request.GET['item'])
            retorno = []
            padres = listaPadres(item.pk)
            for padre in padres:
                retorno.append({'pk_id': padre.pk})
            hijos = listaDescendientes(item)
            hijos.pop(0)
            for hijo in hijos:
                if Items_x_LBase.objects.filter(item=hijo).__len__() > 0:
                    print 'hola'
                    retorno.append({'pk_id': hijo.pk})
            return HttpResponse(simplejson.dumps(retorno),
                                content_type='application/json')
        except Exception:
            print sys.exc_info()
            return HttpResponse(simplejson.dumps(''),
                                content_type='application/json')


def itemsParaSolicitud(idItem):
    """
    Metodo para realizar la verificacion del item para poder ingresar a la lista
    que se envia en el metodo que lo llama.
    :param idItem: id del item a verificar si existe en alguna solicitud valida
    o existe alguna relacion que invalide la seleccion de este item.
    :type idItem: integer
    :return: Bandera para saber si puede o no formar parte de una solicitud
    :rtype: Boolean
    """
    solicitud = Solicitud.objects.filter(item__pk=idItem)
    for sol in solicitud:
        if sol.activo and sol.estado not in ['Rechazado', 'Ejecutado']:
            return True
    if Item.objects.get(pk=idItem).estado == 'revision':
        return True
    for item in Item.objects.filter(item_padre=idItem):
        if item.estado == 'revision':
            return True
    for lb in Items_x_LBase.objects.filter(item__pk=idItem):
        if lb.lb.estado == 'comprometida':
            return True
    return False


def calcularImpacto(item):
    impacto = 0
    padres = listaPadres(item.pk)
    hijos = listaDescendientes(item)
    for padre in padres:
        papa = Item.objects.get(pk=padre)
        impacto += papa.complejidad
    for hijo in hijos:
        impacto += hijo.complejidad
    return impacto


def listaDescendientes(item):
    hijos = Item.objects.filter(item_padre=item.id).order_by('id')
    for i in hijos:
        print '   item hijos: ', i.nombre
    lista = [item]
    if not hijos:
        return lista
    else:
        for h in hijos:
            lista = lista + listaDescendientes(h)
        return lista


def listaPadres(idItem):
    items_padre = []
    i_actual = Item.objects.get(id=idItem)
    while i_actual.item_padre != 0:
        i_actual = Item.objects.get(id=i_actual.item_padre)
        if i_actual not in items_padre:
            items_padre.append(i_actual)
    return items_padre


def listaDescendientesDirectos(request):
    """
    Lista los descendientes directos para verificar el cambio realizado
    :param request: Contiene informacion de la pagina
    :type request: dajngo.http.HttpRequest
    :return: Listado de descendientes
    :rtype: list json
    """
    if request.is_ajax():
        item = Item.objects.get(pk=request.GET['idItem'])
        retorno = []
        hijos = Item.objects.filter(item_padre=item.pk)
        for hijo in hijos:
            retorno.append({'pk_id': hijo.pk, 'nombre': hijo.nombre})
        return HttpResponse(simplejson.dumps(retorno),
                            content_type='application/json')


def verificarSolicitud(request):
    """
    Vista para verificar e ingresar a todos a la LB de vuelta
    :param request: Contiene informacion de la pagina que lo llamo
    :type request: django.http.HttpRequest
    :return: Vista para mostrar todos los items de desarrollo
    :rtype: django.http.response.HttpResponseRedirect
    """
    item = Item.objects.get(pk=request.GET['idItem'])
    solicitud = Solicitud.objects.get(item__pk=item.pk,
                                      estado='Ejecucion')
    with transaction.atomic():
        try:
            item.estado = 'revision-bloq'
            item.save()
            messages.success(request, 'El item ha sido verificado.')
        except Exception:
            print sys.exc_info()
            messages.error(request, 'Ha ocurrido un error al verificar '
                                    'este item.')

    if solicitud.item.filter(estado='revision-desbloq').__len__() == 0:
        try:
            with transaction.atomic():
                for it in solicitud.item.all():
                    hijos = Item.objects.filter(item_padre=it.pk)
                    for hijo in hijos:
                        hijo.estado = 'bloqueado'
                        hijo.save()
                    it.estado = 'bloqueado'
                    it.save()
                for lb in solicitud.lb_relacionadas.all():
                    lb.estado = 'cerrado'
                    lb.save()
                    HistorialLineabase.objects.create(
                        id_usuario=solicitud.id_usuario,
                        tipo_operacion=lb.estado,
                        id_solicitud=solicitud.pk,
                        linea_base=lb
                    )
                solicitud.estado = 'Ejecutado'
                solicitud.save()
            messages.success(request, 'La solicitud ha sido ejecutada con '
                                      'exito, la/s linea/s base/s asociada/s '
                                      'han sido restauradas.')
        except Exception:
            print sys.exc_info()
            messages.error(request, 'Ha ocurrido un error al intentar procesar '
                                    'la finalizacion de la solicitud.')
    return HttpResponseRedirect(
        reverse('sigma:adm_i', args=[request.GET['idFase']]))