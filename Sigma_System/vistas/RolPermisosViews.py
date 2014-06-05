from django.shortcuts import render
from django.http import *
from Sigma_System.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import math


@login_required(login_url='/login/')
def adm_roles(request):
    permisos = request.session['permisos']
    roles_list = Rol.objects.order_by('id')
    return render(request, 'AdministradorRoles.html', {'roles_list': roles_list,
                                                       'permisos': permisos,
                                                       'username': request.user.username})


@login_required(login_url='/login/')
def add_roles(request):
    """
    Vista que maneja la asignacion de permisos.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
        permisos = request.POST.getlist('permisos')
        for p in permisos:
            rol.permisos.add(Permiso.objects.get(id=p))
        messages.success(request, 'El rol "'+rol.nombre+'" ha sido creado con \u00E9xito')
    else:
        permisos = Permiso.objects.all()
        modulo = int(math.ceil(permisos.__len__()/4))
        return render(request, 'Agregar_Rol.html', {'permisos': permisos, 'modulo': modulo})
    return HttpResponseRedirect('/ss/rol/')


@login_required(login_url='/login/')
def del_roles(request, id):
    nombre = Rol.objects.get(id=id).nombre
    Rol.objects.get(id=id).delete()
    messages.error(request, 'El rol "'+nombre+'" ha sido eliminado')
    return HttpResponseRedirect('/ss/rol/')


@login_required(login_url='/login/')
def mod_roles(request, id):
    rol = Rol.objects.get(id=id)
    todoLosPermisos = Permiso.objects.all()
    permisosDelRol = rol.permisos.all()
    permisosAux = []
    for p in todoLosPermisos:
        if p in permisosDelRol:
            diccionario = {'nombre': p.nombre, 'id': p.id, 'ban': "checked"}
            permisosAux.append(diccionario)
        else:
            diccionario = {'nombre': p.nombre, 'id': p.id, 'ban': ""}
            permisosAux.append(diccionario)
    if request.method == 'POST':
        rol.permisos.clear()
        rol.nombre = request.POST['nombre']
        rol.descripcion = request.POST['descripcion']
        rol.save()
        permisos = request.POST.getlist('permisos')
        for p in permisos:
                rol.permisos.add(Permiso.objects.get(id=p))
        messages.info(request, 'El rol: '+rol.nombre+' ha sido modificado con \u00E9xito')
    else:
        modulo = int(math.ceil(permisosAux.__len__()/4))
        return render(request, 'ModificarRol.html', {'rol': rol,
                                                     'permisos': permisosAux,
                                                     'modulo': modulo})
    return HttpResponseRedirect('/ss/rol/')


@login_required(login_url='/login/')
def buscar_roles(request):
    """
    Vista que maneja la busqueda de roles.
    """
    if request.method == 'POST':
        buscar = request.POST['busqueda']
        rol = Rol.objects.filter(nombre=buscar)
        if rol.__len__() == 0:
            messages.error(request, 'No existen coincidencias')
        return render(request, 'BusquedaRol.html', {'roles': rol})
    return HttpResponseRedirect('/ss/rol/')