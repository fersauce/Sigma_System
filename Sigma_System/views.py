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
            if user.__len__() == 0:
                user = User.objects.filter(email=form.cleaned_data['email'])
                if user.__len__() == 0:
                    user = Usuario.objects.filter(ci=form.cleaned_data['ci'])
                    if user.__len__() == 0:
                        usuario = User.objects.create(username=form.cleaned_data['nombre_usuario'],
                                                      first_name=form.cleaned_data['nombre'],
                                                      last_name=form.cleaned_data['apellido'],
                                                      email=form.cleaned_data['email'],
                                                      password=make_password(form.cleaned_data['contrasenha']))
                        Usuario.objects.create(user=usuario, ci=form.cleaned_data['ci'],
                                                       direccion=form.cleaned_data['direccion'],
                                                       tel=form.cleaned_data['tel'],
                                                       estado=True)
                        return HttpResponseRedirect('/ss/adm_u/')
                    else:
                        form = FormAltaUsuario()
                        return render(request, 'Alta Usuario.html', {'form': form, 'alerta': 'Ya existe este ci'})
                else:
                    form = FormAltaUsuario()
                    return render(request, 'Alta Usuario.html', {'form': form, 'alerta': 'Ya existe este e-mail'})
            else:
                form = FormAltaUsuario()
                return render(request, 'Alta Usuario.html', {'form': form, 'alerta': 'Ya existe este username'})
        else:
            return HttpResponseRedirect('/ss/adm_u/')
    else:
        form = FormAltaUsuario()
    return render(request, 'Alta Usuario.html', {'form': form})


@login_required(login_url='/login/')
def adm_usuario(request):
    user = User.objects.all()
    return render(request, 'Administrador Usuario.html', {'user': user })


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
def adm_roles(request):
    roles = Rol.objects.order_by('id')
    return render(request, 'AdministradorRoles.html', {'roles': roles })


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
    else:
        permisos = Permiso.objects.all()
        return render(request, 'Agregar_Rol.html', {'permisos': permisos})
    return HttpResponseRedirect('/ss/adm_r/')


@login_required(login_url='/login/')
def del_roles(request, id):
    Rol.objects.get(id=id).delete()
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
        return render(request, 'BusquedaRol.html', {'roles': rol})
    return HttpResponseRedirect('/ss/adm_r/')

