from random import choice
import string
import simplejson
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from Sigma_System.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from decoradores import permisos_requeridos
from funciones_aux import permisos_disponibles
from django.core.urlresolvers import reverse
from Sigma_System.models import Rol, UsuarioRol, Fase, Item


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
                    request.session['userpk'] = username
                    request.session['permisos'] = permisos_disponibles(request, 0, 0, -1)
                    #if 'super_us' in request.session['permisos']:
                    return HttpResponseRedirect(reverse('sigma:inicio'))
                    #else:
                    #return HttpResponseRedirect(reverse('sigma:adm_proy'))
            else:
                messages.error(request, 'Username o contrasenha incorrecta')
    else:
        form = FormLogin()
    return render(request, 'login.html', {'form': form, })


@login_required(login_url='/login/')
def inicio(request):
    return render(request, 'principal.html', {'user1': request.user.username,
                                              'permisos': request.session['permisos']})


@login_required(login_url='/login/')
def cerrarsesion(request):
    logout(request)
    return iniciarsesion(request)


@login_required(login_url='/login/')
@permisos_requeridos(['crear_us'], 'sigma:adm_u', 'agregar usuario')
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
                    cid = form.cleaned_data['ci']
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
@permisos_requeridos('eliminar_us', 'sigma:adm_u', 'eliminar usuario')
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
@permisos_requeridos(['modificar_us'], 'sigma:adm_u', 'modificar usuario')
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
@permisos_requeridos(['ver_us'], 'sigma:inicio', 'administrar usuarios')
def adm_usuario(request):
    permisos = request.session['permisos']
    user_list = User.objects.exclude(is_active=True, id=request.user.id)
    return render(request, 'ListarUsr.html', {'user_list': user_list,
                                              'permisos': permisos,
                                              'username': request.user.username})


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
    return render(request, 'verDetalle.html', {'user': user})



@login_required(login_url='/login/')
def cambiar(request, us):
    """
    vista utilizada para que el administrador cambie la contrasenha
    de cualquier usuario
    """
    if request.method == 'POST':
        usA=User.objects.get(id=us)
        direc=usA.email
        passNueva=request.POST['passNueva']
        confirmacion=request.POST['conf']
        if passNueva == confirmacion:
            contenido = render_to_string('mailing/recuperacion_password.html',
                                         {'pass': passNueva})
            correo = EmailMessage('Restablecimiento de Pass de SS', contenido,to=[direc])
            correo.content_subtype = "html"
            correo.send()
            nuevo=make_password(confirmacion)
            usA.password = nuevo
            usA.save()
            messages.info(request, 'Contrasenha cambiada con exito')
        else:
            messages.error(request, 'Las contrasenhas no coinciden')
            return render(request, 'cambiarPass2.html', {'id':us,'user':usA})
    else:
        return render(request, 'cambiarPass2.html', {'id':us})

    return HttpResponseRedirect('/ss/inicio/')


@login_required(login_url='/login/')
def del_roles(request, id):
    nombre = Rol.objects.get(id=id).nombre
    Rol.objects.get(id=id).delete()
    messages.error(request, 'El rol: '+nombre+', ha sido eliminado')
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


def redireccion(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('sigma:inicio'))
    else:
        return HttpResponseRedirect(reverse('sigma:login'))


def cambiarPass(request):
    """
    Metodo en el que el usuario cambia su pass
    """
    us = request.user
    if request.method == 'POST':
        #user = User.objects.filter(username=request.POST['un'])

        #if user:

            passVieja= request.POST['passVieja']
            viejoConHash=make_password(passVieja)
            #valor=user.password
            #valor=us.password
            passNueva=request.POST['passNueva']
            confirmacion=request.POST['passNueva2']
            if passNueva == confirmacion:

                nuevo=make_password(confirmacion)
                us.password = nuevo
                us.save()
                messages.info(request, 'Contrasenha cambiada con exito')
            else:
                messages.error(request, 'Las contrasenhas no coinciden')
                return render(request, 'cambiarPass.html')
        #else:
         #   messages.error(request,'El usuario no existe' )
          #  return render(request, 'cambiarPass.html')
    else:
        return render(request, 'cambiarPass.html')
    return HttpResponseRedirect('/ss/inicio/')
@login_required(login_url='/login/')

def asignar_roles(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        roles = request.POST.getlist('roles')
        for rol_i in roles:
            rol = Rol.objects.get(id=rol_i)
            UsuarioRol.objects.create(usuario=user.usuario, rol=rol, idProyecto=0, idFase=0, idItem=0)
        messages.success(request, 'Asignacion correcta de roles del usuario "' + user.username + '"')
    else:
        roles = Rol.objects.all()
        roles_usr = user.usuario.roles.all()
        if roles.__len__() != roles_usr.__len__():
            rol2 = []
            for r in roles:
                if r not in roles_usr:
                    rol2.append(r)
            return render(request, 'AsignarRol.html', {'roles': rol2, 'user': user})
        else:
            messages.info(request, 'El usuario "' + user.username + '" posee todos los roles')
    return HttpResponseRedirect(reverse('sigma:adm_u'))


@login_required(login_url='/login/')
def desasignar_roles(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        roles = request.POST.getlist('roles')
        user.usuario.roles.clear()
        for rol_i in roles:
            rol = Rol.objects.get(id=rol_i)
            UsuarioRol.objects.create(usuario=user.usuario, rol=rol, idProyecto=0, idFase=0, idItem=0)
        messages.success(request, 'Desasignacion correcta de roles del usuario "' + user.username + '"')
    else:
        #roles = user.usuario.roles.all()
        roles = user.usuario.roles.all().filter(usuariorol__idProyecto=0,
                                                usuariorol__idFase=0,
                                                usuariorol__idItem=0)
        if roles.__len__() != 0:
            return render(request, 'DesasignarRol.html', {'roles': roles, 'user': user})
        else:
            messages.info(request, 'El usuario "' + user.username + '" no posee ningun rol')
    return HttpResponseRedirect(reverse('sigma:adm_u'))


def dibujar_grafo(request, idp):
    if request.is_ajax():
        fases = Fase.objects.filter(proyecto__id=idp).order_by('id')
        items_lista = []
        lista_ady2 = {}
        for f in fases:
            items = Item.objects.filter(tipoItems__fase=f).order_by('id')
            for i in items:
                items_lista.append(i)
        for i in items_lista:
            iden_padre = str('Fase ' + str(i.tipoItems.fase.posicionFase) + ':' + i.nombre)
            lista_ady2[iden_padre] = []
            hijos = Item.objects.filter(item_padre=i.id).order_by('id')
            for h in hijos:
                iden_hijo = str('Fase ' + str(h.tipoItems.fase.posicionFase) + ':' + h.nombre)
                lista_ady2[iden_padre].append(iden_hijo)
        #lista_ady = {'dos': [], 'uno': ['dos']}
        return HttpResponse(simplejson.dumps(lista_ady2), content_type='application/json')
    return render(request, 'grafo_sencillo/index_.html', {'direc': idp, 'objeto': 'Proyecto'})


def dibujar_grafo_defase(request, idf):
    if request.is_ajax():
        fase = Fase.objects.get(id=idf)
        #items_lista = []
        lista_ady2 = {}
        items = Item.objects.filter(tipoItems__fase=fase).order_by('id')
        for i in items:
            iden_padre = str('Fase ' + str(i.tipoItems.fase.posicionFase) + ':' + i.nombre)
            lista_ady2[iden_padre] = []
            hijos = Item.objects.filter(item_padre=i.id, tipoItems__fase=fase).order_by('id')
            for h in hijos:
                iden_hijo = str('Fase ' + str(h.tipoItems.fase.posicionFase) + ':' + h.nombre)
                lista_ady2[iden_padre].append(iden_hijo)
        #lista_ady = {'dos': [], 'uno': ['dos']}
        return HttpResponse(simplejson.dumps(lista_ady2), content_type='application/json')
    dire = 'fase/' + str(idf)
    return render(request, 'grafo_sencillo/index_.html', {'direc':dire, 'objeto':'Fase'})


def dibujar_grafo_deitem(request, idi):
    if request.is_ajax():
        lista_ady2 = {}
        item = Item.objects.get(id=idi)
        iden_act = str('Fase ' + str(item.tipoItems.fase.posicionFase) + ':' + item.nombre)

        #meter en la lista de adyacencia al item padre si tiene
        item_padre = Item.objects.filter(id=item.item_padre)
        if item_padre:
            iden_padre = str('Fase ' + str(item_padre[0].tipoItems.fase.posicionFase) + ':' + item_padre[0].nombre)
            lista_ady2[iden_padre] = []
            lista_ady2[iden_padre].append(iden_act)

        #meter en la lista de adyacencia al item en cuestion
        lista_ady2[iden_act] = []
        hijos = Item.objects.filter(item_padre=item.id).order_by('id')

        #meter a los hijos en la lista de adyacencia
        for h in hijos:
            iden_hijo = str('Fase ' + str(h.tipoItems.fase.posicionFase) + ':' + h.nombre)
            lista_ady2[iden_act].append(iden_hijo)
            lista_ady2[iden_hijo] = []

        return HttpResponse(simplejson.dumps(lista_ady2), content_type='application/json')
    dire = 'item/' + str(idi)
    return render(request, 'grafo_sencillo/index_.html', {'direc':dire, 'objeto':'Item'})