from Sigma_System.models import UsuarioRol


def permisos_disponibles(user=None, nivel=0, idp=0, idf=0):
    """
        Metodo que empaqueta el total de permisos de un usuario

        @param user: el usuario ha ser gestionado
        @param nivel: el nivel de inspeccion de los permisos del usuario ha ser filtrados
        @param idp: id del proyecto a ser filtrado
        @param idf: id de la fase a ser filtrado
    """
    roles = None
    if nivel == 0:
        roles = user.usuario.roles.all()
    if nivel != 0:
        usu_roles = UsuarioRol.objects.filter(usuario=user.usuario, idProyecto=idp)
        roles = []
        for u_r in usu_roles:
            roles.append(u_r.rol)
    permisos_ = []
    for rol in roles:
        for permiso in rol.permisos.all():
            if permiso not in permisos_:
                permisos_.append(permiso.codigo)
    return permisos_