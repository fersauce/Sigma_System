from django.shortcuts import render
from Sigma_System.models import Proyecto, Comite, UsuarioPorComite, \
    UsuariosXProyecto


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
    usuProyec = UsuariosXProyecto.objects.filter(proyecto=proyecto).exclude(
        lider=True)

    return render(request, 'administrarcomite.html',
                  {'proyecto': proyecto, 'comite': comite,
                   'usuComite': usuarios, 'usuariosProyecto': usuProyec})


def agregarUsuarios(request, idProyect):
    pass
