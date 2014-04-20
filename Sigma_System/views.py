import datetime
from random import choice
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from Sigma_System.forms import RecuperarPassForm, AltaProyectoForm
from Sigma_System.models import FormLogin, FormAltaUsuario, Usuario, Proyecto, \
    Fase
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
            user = User.objects.filter(
                username=form.cleaned_data['nombre_usuario'])
            if user.__len__() == 0:
                user = User.objects.filter(email=form.cleaned_data['email'])
                if user.__len__() == 0:
                    user = Usuario.objects.filter(ci=form.cleaned_data['ci'])
                    if user.__len__() == 0:
                        usuario = User.objects.create(
                            username=form.cleaned_data['nombre_usuario'],
                            first_name=form.cleaned_data['nombre'],
                            last_name=form.cleaned_data['apellido'],
                            email=form.cleaned_data['email'],
                            password=make_password(
                                form.cleaned_data['contrasenha']))
                        Usuario.objects.create(user=usuario,
                                               ci=form.cleaned_data['ci'],
                                               direccion=form.cleaned_data[
                                                   'direccion'],
                                               tel=form.cleaned_data['tel'],
                                               estado=True)
                        return HttpResponseRedirect('/ss/adm_u/')
                    else:
                        form = FormAltaUsuario()
                        return render(request, 'Alta Usuario.html',
                                      {'form': form,
                                       'alerta': 'Ya existe este ci'})
                else:
                    form = FormAltaUsuario()
                    return render(request, 'Alta Usuario.html', {'form': form,
                                                                 'alerta': 'Ya existe este e-mail'})
            else:
                form = FormAltaUsuario()
                return render(request, 'Alta Usuario.html', {'form': form,
                                                             'alerta': 'Ya existe este username'})
        else:
            return HttpResponseRedirect('/ss/adm_u/')
    else:
        form = FormAltaUsuario()
    return render(request, 'Alta Usuario.html', {'form': form})


@login_required(login_url='/login/')
def adm_usuario(request):
    user = User.objects.all()
    return render(request, 'Administrador Usuario.html', {'user': user})


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


################################################################################
################################################################################
#######################       PROYECTO        ##################################
################################################################################
################################################################################
def administrar_proyecto(request):
    """
    Vista para acceder a la administracion de proyectos.
    """
    proyectos = Proyecto.objects.all()
    return render_to_response('administrarproyectos.html',
                              {'proyectos': proyectos},
                              context_instance=RequestContext(request))


def alta_proyecto(request):
    """
    Vista que realiza la creacion de un nuevo proyecto
    """
    if request.method == 'POST':
        form = AltaProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = Proyecto.objects.filter(
                nombre=form.cleaned_data['nombreProyecto'])
            if proyecto.__len__() == 0:
                fecha = datetime.datetime.now()
                fecha2 = fecha + datetime.timedelta(
                    days=form.cleaned_data['duracion'])
                print str(fecha) + '\n' + str(fecha2)
                nuevoProyecto = Proyecto.objects.create(
                    nombre=form.cleaned_data['nombreProyecto'],
                    fechaCreacion=fecha,
                    descripcion=form.cleaned_data['descripcion'],
                    duracion=form.cleaned_data['duracion'],
                    complejidad=0,
                    costo=0,
                    estado='Pendiente',
                    nroFases=0,
                    nroMiembros=0,
                    fechaInicio=fecha,
                    fechaFinalizacion=fecha2)
                print Usuario.objects.get(user=User.objects.get(
                    username=form.cleaned_data['lider'])).__str__()
                print str(form.cleaned_data['duracion'])
                print str(form.cleaned_data['lider'])
                return HttpResponseRedirect('/ss/proyecto/')
            else:
                form = AltaProyectoForm()
                return render(request, 'proyectoalta.html', {'form': form,
                                                             'alerta': 'Proyecto ya existente con ese nombre'})
    else:
        print '3'
        form = AltaProyectoForm()
    return render_to_response('proyectoalta.html', {'form': form},
                              context_instance=RequestContext(request))


def modificar_proyecto(request, idProyecto):
    """
    Vista para realizar la modificacion de datos del proyecto
    """
    pass


def baja_proyecto(request, idProyecto):
    """
    Vista para realizar la baja de un proyecto.
    """
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(pk=idProyecto)
        proyecto.delete()
        print 'Hola'
    elif request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyecto)
        if proyecto.estado == 'Iniciado':
            return render(request, 'proyectobaja.html', {
                'alerta': 'No se puede suprimir el proyecto'})
        else:
            return render(request, 'proyectobaja.html',
                          {'idProyecto': idProyecto})
        print 'Chau'
    return HttpResponseRedirect('/ss/proyecto/')


def buscar_proyecto(request):
    """
    Vista para realizar la busqueda de un proyecto
    """
    pass


################################################################################
################################################################################
#########################          FASES          ##############################
################################################################################
################################################################################


def administrar_fases(request, idProyect):
    """
    Vista para realizar la administracion de las fases de un proyecto
    :param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    fases = Fase.objects.filter(proyecto=proyecto)
    return render(request, 'administrarfases.html',
                  {'proyecto': proyecto, 'fases': fases})


def alta_fase(request):
    """
    Vista para realizar la alta de una fase
    """
    pass


def modificar_fase(request):
    """
    Vista para realizar la modificacion de datos de una fase
    """
    pass


def baja_fase(request):
    """
    Vista para realizar la baja de una fase
    """
    pass


def buscar_fase(request):
    """
    Vista para realizar la busqueda de fases.
    """
    pass