from Sigma_System.models import UsuarioRol, UsuariosXProyecto


def permisos_disponibles(request, nivel=0, idp=0, idf=0):
    """
        Metodo que empaqueta el total de permisos de un usuario
        @param request: contiene la informacion de la pagina que solicito la vista
        @type request: django.http.HttpRequest
        @param nivel: el nivel de inspeccion de los permisos del usuario ha ser filtrados
        @type nivel: int
        @param idp: id del proyecto a ser filtrado
        @type idp: int
        @param idf: id de la fase a ser filtrado
        @type: int
        @return: devuelve los permisos del usuario
        @rtype: list
    """
    roles = None
    if nivel == 0:
        roles = request.user.usuario.roles.all()
    if nivel != 0:
        posible_lider = UsuariosXProyecto.objects.filter(usuario=request.user.usuario,
                                                         proyecto__id=idp, lider=True)
        if posible_lider:
            if posible_lider[0].lider or 'super_us' in request.session['permisos']:
                roles = request.user.usuario.roles.all()
        else:
            usu_roles = UsuarioRol.objects.filter(usuario=request.user.usuario, idProyecto=idp, idFase=idf)
            roles = []
            for u_r in usu_roles:
                roles.append(u_r.rol)

    permisos_ = []
    for rol in roles:
        for permiso in rol.permisos.all():
            if permiso not in permisos_:
                permisos_.append(permiso.codigo)
    if idf >= 0:
        if 'modificar_pr' in request.session['permisos'] and 'modificar_pr' not in permisos_:
            permisos_.append('modificar_pr')
        if 'adm_pr' in request.session['permisos'] and 'adm_pr' not in permisos_:
            permisos_.append('adm_pr')
        if 'des_pr' in request.session['permisos'] and 'des_pr' not in permisos_:
            permisos_.append('des_pr')
        if 'gest_pr' in request.session['permisos'] and 'gest_pr' not in permisos_:
            permisos_.append('gest_pr')
    return permisos_