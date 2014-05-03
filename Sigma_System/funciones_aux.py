def permisos_disponibles(user):
    '''
        Metodo que sirve que empaqueta el total de permisos de un usuario
    '''
    roles = user.usuario.roles.all()
    permisos_ = []
    for rol in roles:
        for permiso in rol.permisos.all():
            if permiso not in permisos_:
                permisos_.append(permiso.codigo)
    return permisos_
