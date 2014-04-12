from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import *
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