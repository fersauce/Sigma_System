import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import sys
from Sigma_System.models import UsuarioPorComite, Solicitud, Proyecto, Fase, \
    Votacion, Item, HistorialLineabase


def administrarVotacion(request):
    usuario = request.user.usuario
    comites = UsuarioPorComite.objects.filter(usuario=usuario)
    proyecto = []
    for comite in comites:
        solicitudes = Solicitud.objects.filter(proyecto=comite.comite.proy)
        if solicitudes.__len__() > 0:
            proyecto.append(comite.comite.proy.pk)
    if proyecto.__len__() == 0:
        return HttpResponseRedirect(reverse('sigma:inicio'))
    proyectos = Proyecto.objects.filter(pk__in=proyecto)
    for proy in proyectos:
        print proy
    return render(request, 'votos_proyectos.html', {'proyectos': proyectos})


def administrarVotacionProyectos(request, idProyecto):
    proyecto = Proyecto.objects.get(pk=idProyecto)
    solicitudes = Solicitud.objects.filter(proyecto=proyecto, estado='Votacion')
    fase = []
    for solicitud in solicitudes:
        if solicitud.fase.pk not in fase:
            fase.append(solicitud.fase.pk)
    if fase.__len__() == 0:
        messages.info(request, 'No tiene solicitudes pendientes de votacion.')
        return HttpResponseRedirect(reverse('sigma:voto_adm'))
    fases = Fase.objects.filter(pk__in=fase)
    return render(request, 'votos_fases.html',
                  {'fases': fases, 'proyecto': proyecto})


def administrarVotacionFase(request, idFase):
    fase = Fase.objects.get(pk=idFase)
    solicitudes = Solicitud.objects.filter(fase=fase, estado='Votacion')
    c = []
    for solicitud in solicitudes:
        a = Votacion.objects.filter(miembro=request.user.usuario,
                                    solicitud=solicitud).first()
        if a:
            c.append(solicitud.pk)
    '''if c.__len__() == 0:
        return HttpResponseRedirect(
            reverse('sigma:voto_adm_proy', args=[fase.proyecto.pk]))'''
    solicitudesFinal = Solicitud.objects.filter(fase=fase,
                                                estado='Votacion').exclude(
        pk__in=c)
    return render(request, 'votos_listado.html',
                  {'proyecto': fase.proyecto, 'fase': fase,
                   'solicitudes': solicitudesFinal})


def realizarVoto(request, idSolicitud, idFase, voto):
    """
    Vista para ejecutar el voto del usuario del comite
    :param request: Contiene la informacion de la pagina que lo solicito
    :type request: django.http.HttpRequest
    :return: pantalla con la solicitud ya votada
    :rtype: django.http.response.HttpResponseRedirect
    """
    if request.method == 'GET':
        solicitud = Solicitud.objects.get(pk=idSolicitud)
        if voto == '0':
            try:
                with transaction.atomic():
                    solicitud.nro_votos_posit += 1
                    solicitud.save()
                    Votacion.objects.create(
                        miembro=request.user.usuario,
                        solicitud=solicitud,
                        fechaVotacion=datetime.datetime.now(),
                        voto=True
                    )
                    if solicitud.nro_votos_posit == 2:
                        solicitud.estado = 'Aprobado'
                        solicitud.fecha_limite = datetime.datetime.now() + datetime.timedelta(
                            days=2)
                        solicitud.save()
                        messages.info(request, 'La solicitud ' +
                                      str(solicitud.codigo) +
                                      ' ha sido aprobada. El '
                                      'solicitante puede ejecutar la '
                                      'solicitud')
                messages.success(request,
                                 'Se ha registrado su voto para '
                                 'la solicitud ' + str(solicitud.codigo))
            except Exception:
                print sys.exc_info()
                messages.error(request,
                               'Ha ocurrido un error al registrar el voto')
        elif voto == '1':
            try:
                with transaction.atomic():
                    solicitud.nro_votos_neg += 1
                    solicitud.save()
                    Votacion.objects.create(
                        miembro=request.user.usuario,
                        solicitud=solicitud,
                        fechaVotacion=datetime.datetime.now(),
                        voto=False
                    )
                    if solicitud.nro_votos_neg == 2:
                        solicitud.estado = 'Rechazado'
                        solicitud.save()
                        for item in solicitud.item.all():
                            for hijo in Item.objects.filter(item_padre=item.pk):
                                hijo.estado = 'bloqueado'
                                hijo.save()
                            item.estado = 'bloqueado'
                            item.save()
                        for lb in solicitud.lb_relacionadas.all():
                            lb.estado = 'cerrado'
                            lb.save()
                            HistorialLineabase.objects.create(
                                id_usuario=request.user.usuario.pk,
                                tipo_operacion=lb.estado,
                                id_solicitud=solicitud.pk,
                                linea_base=lb
                            )
                        messages.info(request, 'La solicitud ' + str(
                            solicitud.codigo) + ' ha sido rechazada. \n Los '
                                                'items han sido liberados')
                messages.success(request,
                                 'Se ha registrado su voto para '
                                 'la solicitud ' + str(solicitud.codigo))
            except Exception:
                print sys.exc_info()
                messages.error(request,
                               'Ha ocurrido un error al registrar el voto')
    return HttpResponseRedirect(
        reverse('sigma:voto_adm_fase', args=[idFase]))