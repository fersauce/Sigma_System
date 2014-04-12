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
            print ("entro en valid")
            print(form.cleaned_data['nombre_usuario'])
            user = User.objects.filter(username=form.cleaned_data['nombre_usuario'])
            print (user)
            if user is not None:
                print ("entro en None 1")
                user = User.objects.filter(email=form.cleaned_data['email'])
                print(form.cleaned_data['email'])
                print (user)
                if user:
                    print ("entro en None 2")
                    user = Usuario.objects.filter(ci=form.cleaned_data['ci'])
                    print(form.cleaned_data['ci'])
                    print (user)
                    if user is None:
                        print ("entro en None 3")
                        '''usuario = User.objects.create(username=form.cleaned_data['nombre_usuario'],
                                                      first_name=form.cleaned_data['nombre'],
                                                      last_name=form.cleaned_data['apellido'],
                                                      email=form.cleaned_data['email'],
                                                      password=make_password(form.cleaned_data['contrasenha']))
                        Usuario.objects.create(user=usuario, ci=form.cleaned_data['ci'],
                                                       direccion=form.cleaned_data['direccion'],
                                                       tel=form.cleaned_data['tel'],
                                                       estado=True)'''
                    else:
                        print "entro aca1"
                        form = FormAltaUsuario()
                        return render(request, 'Alta Usuario.html', {'form': form, 'alerta': 'Ya existe este ci'})
                else:
                    print "entro aca2"
                    form = FormAltaUsuario()
                    return render(request, 'Alta Usuario.html', {'form': form, 'alerta': 'Ya existe este e-mail'})
            else:
                print "entro aca3"
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