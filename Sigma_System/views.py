from random import choice
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from Sigma_System.forms import RecuperarPassForm, FormLogin, FormAltaUsuario
from Sigma_System.models import Usuario, Rol, Permiso
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def iniciarsesion(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'principal.html', {'user': username, })
    else:
        form = FormLogin()
    return render(request, 'login.html', {'form': form, })


@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'principal.html')


@login_required(login_url='/login/')
def cerrarsesion(request):
    logout(request)
    return iniciarsesion(request)


@login_required(login_url='/login/')
def alta_usuario(request):
    if request.method == 'POST':
        form = FormAltaUsuario(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data['nombre_usuario'])
            user_n = form.cleaned_data['nombre_usuario']
            if user.__len__() == 0:
                e_mail = form.cleaned_data['email']
                user = User.objects.filter(email=form.cleaned_data['email'])
                if user.__len__() == 0:
                    cid=form.cleaned_data['ci']
                    user = Usuario.objects.filter(ci=form.cleaned_data['ci'])
                    if user.__len__() == 0:
                        usuario = User.objects.create(username=form.cleaned_data['nombre_usuario'],
                                                      first_name=form.cleaned_data['nombre'],
                                                      last_name=form.cleaned_data['apellido'],
                                                      email=form.cleaned_data['email'],
                                                      password=make_password(form.cleaned_data['contrasenha']),
                                                      is_active=True)
                        Usuario.objects.create(user=usuario, ci=form.cleaned_data['ci'],
                                                       direccion=form.cleaned_data['direccion'],
                                                       tel=form.cleaned_data['tel'],
                                                       estado=True)
                        messages.success(request, 'El usuario "'+usuario.username+'" ha sido creado con exito')
                        user = User.objects.filter(is_active=True)
                        return render(request, 'Administrador Usuario.html', {'user': user})
                    else:
                        form = FormAltaUsuario()
                        messages.error(request, 'El ci "'+cid+'" ya existe')
                        return render(request, 'Alta Usuario.html', {'form': form})
                else:
                    form = FormAltaUsuario()
                    messages.error(request, 'El e-mail "'+e_mail+'" ya existe')
                    return render(request, 'Alta Usuario.html', {'form': form})
            else:
                form = FormAltaUsuario()
                messages.error(request, 'El username "'+user_n+'" ya existe')
                return render(request, 'Alta Usuario.html', {'form': form})
        else:
            messages.error(request, 'Formulario invalido')
            user = User.objects.filter(is_active=True)
            return render(request, 'Administrador Usuario.html', {'user': user})
    else:
        form = FormAltaUsuario()
    return render(request, 'Alta Usuario.html', {'form': form})


@login_required(login_url='/login/')
def baja_usuario(request, us):
    """
    vista utilizada para dar de baja un usuario, baja logica
    """
    user=User.objects.get(id=us)
    user.is_active=False
    nombre = user.username
    user.save()
    user = User.objects.filter(is_active=True)
    messages.error(request, 'El usuario "'+nombre+'" ha sido eliminado')
    return render(request, 'Administrador Usuario.html', {'user': user})


@login_required(login_url='/login/')
def modificar_usuario(request, us, pag):
    """
    vista utilizada para dar de baja a un usuario, baja logica
    """
    user = User.objects.get(id=us)
    direccion = '/ss/adm_u/?page = '+ pag
    if request.method == 'POST':
        user.usuario.direccion = request.POST['direccion']
        user.usuario.tel = request.POST['tel']
        user.usuario.save()
        nombre = user.username
        messages.info(request, 'usuario: '+nombre+', modificado correctamente')
    else:
        return render(request, 'modificarUsuario.html', {'user': user, 'pag': pag})
    return HttpResponseRedirect(direccion)


@login_required(login_url='/login/')
def adm_usuario(request):
    user_list = User.objects.filter(is_active=True)
    paginator = Paginator(user_list, 2)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    return render(request, 'Administrador Usuario.html', {"user": users})


def recuperarPass(request):
    """
    Vista que es utilizada para la regeneracion del pass de un usuario
    """
    if request.method == 'POST':
        formulario = RecuperarPassForm(request.POST, request.FILES)
        """
        Variable que representa al formulario
        """
        if formulario.is_valid():
            password = generar_nuevo_pass(request, formulario.cleaned_data['correo'])
            contenido = render_to_string('mailing/recuperacion_password.html', {'pass': password})
            correo = EmailMessage('Restablecimiento de Pass de SS', contenido,
                                  to=[formulario.cleaned_data['correo']])
            correo.content_subtype = "html"
            correo.send()
            return HttpResponseRedirect('/ss/login/')
    else:
        formulario = RecuperarPassForm()
    return render_to_response('recuperarpassform.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


def generar_nuevo_pass(request, correo):
    """
    Metodo que genera el nuevo pass para el usuario.
    """
    if correo is not None:
        user = User.objects.get(email=correo)
        password = ''.join([choice(string.letters + string.digits) for i in range(10)])
        user.password = make_password(password)
        user.save()
        return str(password)
    return None


@login_required(login_url='/login/')
def buscar_usuario(request):
    """
    vista utilizada para buscar un usuario
    """
    if request.method == 'POST':
        buscar = request.POST['valor_buscado']
        user = User.objects.filter(username=buscar)
        if user.__len__() == 0:
            messages.error(request, 'No existen coincidencias')
        return render(request, 'busquedUsuario.html', {'user': user})
    return HttpResponseRedirect('/ss/adm_u/')



@login_required(login_url='/login/')
def ver_detalle(request, us):
    """
    vista utilizada para dar los demas datos de un usuario,
    pero sin modificarlos
    """
    user = User.objects.filter(is_active=True, id = us)
    return render(request, 'verDetalle.html', {'user': user })

@login_required(login_url='/login/')
def adm_roles(request):
    roles_list = Rol.objects.order_by('id')
    paginator = Paginator(roles_list, 2)

    page = request.GET.get('page')
    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        roles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        roles = paginator.page(paginator.num_pages)

    return render(request, 'AdministradorRoles.html', {'roles': roles})


@login_required(login_url='/login/')
def add_roles(request):
    """
    Vista que maneja la asignacion de roles.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
        permisos = request.POST.getlist('permisos')
        for p in permisos:
            rol.permisos.add(Permiso.objects.get(id=p))
        messages.success(request, 'El rol: '+rol.nombre+', ha sido creado con exito')
    else:
        permisos = Permiso.objects.all()
        return render(request, 'Agregar_Rol.html', {'permisos': permisos})
    return HttpResponseRedirect('/ss/adm_r/')


@login_required(login_url='/login/')
def del_roles(request, id):
    nombre = Rol.objects.get(id=id).nombre
    Rol.objects.get(id=id).delete()
    messages.error(request, 'El rol: '+nombre+', ha sido eliminado')
    return HttpResponseRedirect('/ss/adm_r/')


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
    rol.permisos.clear()
    if request.method == 'POST':
        rol.nombre = request.POST['nombre']
        rol.descripcion = request.POST['descripcion']
        rol.save()
        permisos = request.POST.getlist('permisos')
        for p in permisos:
                rol.permisos.add(Permiso.objects.get(id=p))
        messages.success(request, 'El rol: '+rol.nombre+' ha sido modificado con exito')
    else:
        return render(request, 'ModificarRol.html', {'rol': rol, 'permisos': permisosAux})
    return HttpResponseRedirect('/ss/adm_r/')


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
    return HttpResponseRedirect('/ss/adm_r/')