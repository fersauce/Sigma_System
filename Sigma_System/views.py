from random import choice
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from Sigma_System.forms import RecuperarPassForm
from Sigma_System.models import FormLogin, FormAltaUsuario, Usuario
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
    return render(request, 'Alta Usuario.html', {'form': form})


@login_required(login_url='/login/')
def adm_usuario(request):
    user = User.objects.all()
    return render(request, 'Administrador Usuario.html', {'user': user })


def recuperarPass(request):
    if request.method == 'POST':
        formulario = RecuperarPassForm(request.POST, request.FILES)
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
    if correo is not None:
        user = User.objects.get(email=correo)
        password = ''.join([choice(string.letters + string.digits) for i in range(10)])
        user.password = make_password(password)
        user.save()
        return str(password)

    return None