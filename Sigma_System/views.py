from random import choice
import string
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from Sigma_System.models import *
from Sigma_System.forms import *
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
                    return render(request, 'principal.html',
                                  {'user': username, })
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
                        return HttpResponseRedirect('/ss/adm_u/')
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
            return HttpResponseRedirect('/ss/adm_u/')
    else:
        form = FormAltaUsuario()
    return render(request, 'Alta Usuario.html', {'form': form})


@login_required(login_url='/login/')
def baja_usuario(request, us):
    """
    vista utilizada para dar de baja un usuario, baja logica
    """
    user = User.objects.get(id=us)
    user.is_active = False
    nombre = user.username
    user.save()
    messages.error(request, 'El usuario "'+nombre+'" ha sido eliminado')
    return HttpResponseRedirect('/ss/adm_u/')


@login_required(login_url='/login/')
def modificar_usuario(request, us):
    """
    vista utilizada para dar de baja a un usuario, baja logica
    """
    user = User.objects.get(id=us)
    #direccion = '/ss/adm_u/?page='+request.session['pag_actual']
    if request.method == 'POST':
        user.first_name=request.POST['nombre']
        user.last_name=request.POST['apellido']
        user.usuario.direccion = request.POST['direccion']
        user.usuario.ci=request.POST['ci']
        user.usuario.tel = request.POST['tel']
        user.usuario.save()
        user.save()
        nombre = user.username
        messages.info(request, 'usuario "'+nombre+'" modificado correctamente')
    else:
        return render(request, 'modificarUsuario.html', {'user': user})
    return HttpResponseRedirect('/ss/adm_u/')


@login_required(login_url='/login/')
def adm_usuario(request):
    user_list = User.objects.filter(is_active=True)
    """paginator = Paginator(user_list, 2)
    page = request.GET.get('page')
    request.session['pag_actual'] = page
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)"""
    return render(request, 'ListarUsr.html', {'user_list': user_list})


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
            password = generar_nuevo_pass(request,
                                          formulario.cleaned_data['correo'])
            contenido = render_to_string('mailing/recuperacion_password.html',
                                         {'pass': password})
            correo = EmailMessage('Restablecimiento de Pass de SS', contenido,
                                  to=[formulario.cleaned_data['correo']])
            correo.content_subtype = "html"
            correo.send()
            return HttpResponseRedirect('/ss/login/')
    else:
        formulario = RecuperarPassForm()
    return render_to_response('recuperarpassform.html',
                              {'formulario': formulario},
                              context_instance=RequestContext(request))


def generar_nuevo_pass(request, correo):
    """
    Metodo que genera el nuevo pass para el usuario.
    """
    if correo is not None:
        user = User.objects.get(email=correo)
        password = ''.join([choice(string.letters
                                   + string.digits) for i in range(10)])
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


def cambiarPass(request):
    """
    Metodo en el que el usuario cambia su pass
    """
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['un'])
        passVieja= request.POST['passVieja']
        viejoConHash=make_password(passVieja)
        valor=user.password
        passNueva=request.POST['passNueva']
        confirmacion=request.POST['passNueva2']
        if passNueva == confirmacion:
            nuevo=make_password(confirmacion)
            user.password = nuevo
            user.save()
            messages.info(request, 'Contrasenha cambiada con exito')
        else:
            messages.error(request, 'Las contrasenhas no coinciden')
    else:
        return render(request, 'cambiarPass.html')
    return HttpResponseRedirect('/ss/inicio/')