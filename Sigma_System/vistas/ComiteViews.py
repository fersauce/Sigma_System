from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import simplejson
import sys
from Sigma_System.models import Proyecto, Comite, UsuarioPorComite, \
    UsuariosXProyecto, Usuario


def ComiteDeCambio(request, idProyect):
    """
    Vista que administra el comite de cambios del proyecto asociado.

    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo.

    @type idProyect: Unicode
    @param idProyect: Contiene el id del proyecto que se va a asociar/desasociar
    usuarios a su comite.

    @rtype django.shortcuts.render
    @return: AdministrarComite.html, pagina en la cual se trabaja con el comite
    del proyecto.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    comite = Comite.objects.get(proy=proyecto)
    usuarios = UsuarioPorComite.objects.filter(comite=comite)
    us = []
    for i in usuarios:
        us.append(i.usuario)
    usuProyec = UsuariosXProyecto.objects.filter(proyecto=proyecto, activo=True)
    if request.method == 'POST':
        usuariosComitePOST = request.POST.getlist('usuariosAsig')
        bandera = False
        print usuariosComitePOST
        if usuariosComitePOST.__len__() % 2 == 0:
            messages.error(request, 'El comite no debe ser par')
            return HttpResponseRedirect(reverse('sigma:adm_proy_comite'))
        for u in usuProyec:
            miembro = usuarios.filter(usuario=u.usuario)
            if miembro:
                print 'es'
            else:
                print 'no es'
            print u.usuario.pk
            if str(u.usuario.pk) in usuariosComitePOST:
                if not miembro:
                    try:
                        UsuarioPorComite.objects.create(
                            comite=comite,
                            usuario=u.usuario
                        )
                        messages.success(request,
                                         'El usuario ' +
                                         u.usuario.user.first_name
                                         + ' ha sido asignado al comite del '
                                           'proyecto ' +
                                         proyecto.nombre)
                        bandera = True
                    except Exception:
                        messages.error(request,
                                       'Ha ocurrido un error interno, favor'
                                       ' contacte al administrador')
                        sys.exc_info()
            else:
                if miembro:
                    try:
                        miembro.delete()
                        messages.success(request,
                                         'El usuario ' +
                                         u.usuario.user.first_name
                                         + ' ha sido desasignado del comite del'
                                           ' proyecto ' +
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
    else:
        pass

    return render(request, 'administrarcomite.html',
                  {'proyecto': proyecto, 'comite': comite,
                   'usuComite': us, 'usuariosProyecto': usuProyec,
                   'permisos': request.session['permisos']})


def agregarUsuarios(request, idProyect):
    """
    Vista que asigna usuarios a un comite de cambios proyecto determinado.

    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo.

    @type idProyect: Unicode
    @param idProyect: Contiene el id del proyecto que se va a asociar/desasociar
    usuarios a su comite.

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    usuarios = UsuariosXProyecto.objects.filter(proyecto=proyecto)
    comite = Comite.objects.get(proy=proyecto)
    usuariosPorComite = UsuarioPorComite.objects.filter(comite=comite)
    if request.method == 'POST':
        usuariosComitePOST = request.POST.getlist('usuariosAsig')
        print 'hola'
        print usuariosComitePOST
        bandera = False
        for u in usuarios:
            if str(u.usuario.pk) in usuariosComitePOST:
                if not usuariosPorComite.get(usuario=u.usuario):
                    try:
                        UsuarioPorComite.objects.create(
                            comite=comite,
                            usuario=u.usuario
                        )
                        messages.success(request,
                                         'El usuario ' +
                                         u.usuario.user.first_name
                                         + ' ha sido asignado al comite del '
                                           'proyecto ' +
                                         proyecto.nombre)
                        bandera = True
                    except Exception:
                        messages.error(request,
                                       'Ha ocurrido un erro interno, favor'
                                       ' contacte al administrador')
            else:
                miembro = usuariosPorComite.get(usuario=u.usuario)
                if miembro:
                    try:
                        miembro.delete()
                        messages.success(request,
                                         'El usuario ' +
                                         u.usuario.user.first_name
                                         + ' ha sido desasignado del comite del'
                                           ' proyecto ' +
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
    else:
        pass

    return render(request, 'administrarcomite.html',
                  {'usuariosProyecto': usuarios, 'proyecto': proyecto,
                   'comite': comite, 'usuarioComite': usuariosPorComite})
