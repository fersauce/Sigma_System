from random import choice
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
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
                        messages.success(request, 'El usuario: '+usuario.username+', ha sido creado con exito')
                        user = User.objects.filter(is_active=True)
                        return render(request, 'Administrador Usuario.html', {'user': user})
                    else:
                        form = FormAltaUsuario()
                        messages.error(request, 'El ci: '+cid+', ya existe')
                        return render(request, 'Alta Usuario.html', {'form': form})
                else:
                    form = FormAltaUsuario()
                    messages.error(request, 'El e-mail: '+e_mail+', ya existe')
                    return render(request, 'Alta Usuario.html', {'form': form})
            else:
                form = FormAltaUsuario()
                messages.error(request, 'El username: '+user_n+', ya existe')
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
    messages.error(request, 'El useario: '+nombre+', fue dado de baja')
    return render(request, 'Administrador Usuario.html', {'user': user})


@login_required(login_url='/login/')
def modificar_usuario(request, us):
    """
    vista utilizada para dar de baja a un usuario, baja logica
    """
    user = User.objects.get(id=us)
    if request.method == 'POST':
        user.usuario.direccion = request.POST['direccion']
        user.usuario.tel = request.POST['tel']
        user.usuario.save()
        nombre = user.username
        messages.success(request, 'usuario: '+nombre+', modificado correctamente')
    else:
        return render(request, 'modificarUsuario.html', {'user': user})
    return HttpResponseRedirect('/ss/adm_u/')


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

################################################################################
################################################################################
#######################       PROYECTO        ##################################
################################################################################
################################################################################
def administrar_proyecto(request):
    """
    Vista para acceder a la administracion de proyectos.
    """
    proyectos = Proyecto.objects.all().order_by('-nombre')
    return render_to_response('administrarproyectos.html',
                              {'proyectos': proyectos,
                               'vacio': 'No se encuentran proyectos '
                                        'registrados',
                               'form': BusquedaProyectoForm()}
                              , context_instance=RequestContext(request))
    '''proyecto_list = Proyecto.objects.all()
    paginator = Paginator(proyecto_list, 2)

    page = request.GET.get('page')
    try:
        proyectos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        proyectos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        proyectos = paginator.page(paginator.num_pages)
    return render(request, 'administrarproyectos.html',
                  {"proyectos": proyectos,
                   'vacio': 'No se encuentran proyectos registrados',
                   'form': forms.BusquedaProyectoForm()})'''


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
                return render(request, 'proyectoalta.html',
                              {'form': form,
                               'alerta': 'Proyecto ya existente '
                                         'con ese nombre'})
    else:
        print '3'
        form = AltaProyectoForm()
    return render_to_response('proyectoalta.html', {'form': form},
                              context_instance=RequestContext(request))


def modificar_proyecto(request, idProyecto):
    """
    Vista para realizar la modificacion de datos del proyecto
    """
    proyecto = Proyecto.objects.get(pk=idProyecto)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        if proyecto.estado == 'Iniciado':
            proyecto.duracion = request.POST['duracion']
        else:
            proyecto.nombre = request.POST['nombre']
            proyecto.descripcion = request.POST['descripcion']
            proyecto.duracion = request.POST['duracion']
            proyecto.fechaFinalizacion = proyecto.fechaInicio + \
                                         datetime.timedelta(
                                             days=int(proyecto.duracion))
            print str(proyecto.fechaFinalizacion) + 'hola' + str(
                datetime.timedelta(days=int(proyecto.duracion)))
        proyecto.save()
        return HttpResponseRedirect('/ss/proyecto')
    return render(request, 'proyectomodificar.html', {'proyecto': proyecto,
                                                      'choices': usuarios})


def baja_proyecto(request, idProyecto):
    """
    Vista para realizar la baja de un proyecto.
    :param idProyecto: pk del proyecto a ser suprimido del sistema.
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyecto)
        if proyecto.estado == 'Iniciado':
            return render(request, 'proyectobaja.html', {
                'alerta': 'No se puede suprimir el proyecto'})
        elif Fase.objects.filter(proyecto=proyecto).__len__() > 0:
            return render(request, 'proyectobaja.html', {
                'alerta': 'No se puede suprimir el proyecto'})
        else:
            proyecto.delete()
    return HttpResponseRedirect('/ss/proyecto/')


def buscar_proyecto(request):
    """
    Vista para realizar la busqueda de un proyecto
    """
    proyectos = []
    if request.method == 'POST':
        form = BusquedaProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['columna'] == '1':
                """
                Si el patron a utilizar es el nombre
                """
                proyectos = Proyecto.objects.filter(
                    nombre=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '2':
                """
                Si el patron a utilizar es la fecha de inicio
                """
                proyectos = Proyecto.objects.filter(
                    fechaInicio=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de culminacion de un
                proyecto
                """
                proyectos = Proyecto.objects.filter(
                    fechaFinalizacion=form.cleaned_data['busqueda'])
    return render(request, 'administrarproyectos.html',
                  {'proyectos': proyectos,
                   'vacio': 'No se encuentran proyectos con ese '
                            'patron de busqueda',
                   'form': BusquedaProyectoForm()})


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
    fases = Fase.objects.filter(proyecto=proyecto).order_by('posicionFase')
    return render(request, 'administrarfases.html',
                  {'proyecto': proyecto, 'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases asociadas a este '
                            'proyecto'})


def alta_fase(request, idProyect):
    """
    Vista para realizar la alta de una fase
    :param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(pk=idProyect)
        fase = Fase.objects.filter(proyecto=proyecto).filter(
            nombre=request.POST['nombre'])
        if fase.__len__() > 0:
            ultFase = Fase(fase.last())
            if request.POST['fechaInicio'] > request.POST['fechaFin']:
                messages.error(request, 'La fecha de Inicio se encuentra'
                                        'mas adelantada que la fecha de fin')
                return render(request, 'fasealta.html',
                              {'proyecto': idProyect, 'fase': fase})
            if ultFase is not None:
                if str(ultFase.fechaFin) > request.POST['fechaInicio']:
                    messages.error(request,
                                   'La fecha de Inicio de esta '
                                   'fase es inferior a la fecha de  '
                                   'fin de la fase anterior')
                    return render(request, 'fasealta.html',
                                  {'fase': fase, 'proyecto': idProyect})
            faseNueva = Fase.objects.create(
                proyecto=proyecto,
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion'],
                posicionFase=Fase.objects.filter(
                    proyecto=proyecto).__len__() + 1,
                estado='Pendiente'
            )
            proyecto.nroFases = Fase.objects.filter(proyecto=proyecto).__len__()
            proyecto.save()
            messages.success(request, 'Fase creada con exito')
            return HttpResponseRedirect(
                '/ss/proyecto/' + str(idProyect) + '/fase/')
        else:
            return render(request, 'fasealta.html',
                          {'proyecto': idProyect,
                           'alerta': 'Nombre de Fase ya existente '
                                     'en este proyecto'})

    return render(request, 'fasealta.html', {'usuarios': usuarios,
                                             'proyecto': idProyect})


def modificar_fase(request, idProyect, idFase):
    """
    Vista para realizar la modificacion de datos de una fase
    :param idProyect: pk del proyecto sobre el cual se esta trabajando
    :param idFase: pk de la fase que se quiere modificar
    """
    fase = Fase.objects.get(pk=idFase)
    fase.fechaInicio = str(fase.fechaInicio)
    fase.fechaFin = str(fase.fechaFin)
    if request.method == 'POST':
        if fase.nombre == request.POST['nombre'] or Fase.objects.get(
                nombre=request.POST['nombre']):
            if fase.posicionFase > 1:
                faseAnt = Fase.objects.get(posicionFase=fase.posicionFase - 1)
                if str(faseAnt.fechaFin) > request.POST['fechaInicio']:
                    return render(request, 'fasemodificar.html',
                                  {'proyecto': idProyect, 'fase': fase,
                                   'alerta': 'La fecha de Inicio de esta fase '
                                             'es inferior a la fecha de '
                                             'fin de la fase anterior'})
            print Proyecto.objects.get(pk=idProyect).nroFases
            if fase.posicionFase < Proyecto.objects.get(pk=idProyect).nroFases:
                faseSig = Fase.objects.get(posicionFase=fase.posicionFase + 1)
                if str(faseSig.fechaInicio) > request.POST['fechaFin']:
                    messages.error(request, 'La fecha de fin de esta fase '
                                            'es superior a la fecha de '
                                            'inicio de la fase siguiente')
                    return render(request, 'fasemodificar.html',
                                  {'proyecto': idProyect, 'fase': fase})
            if request.POST['fechaInicio'] > request.POST['fechaFin']:
                messages.error(request, 'La fecha de Inicio se encuentra '
                                        'mas adelantada que la fecha de fin')
                return render(request, 'fasemodificar.html',
                              {'proyecto': idProyect, 'fase': fase})
            fase.nombre = request.POST['nombre']
            fase.descripcion = request.POST['descripcion']
            fase.fechaInicio = request.POST['fechaInicio']
            fase.fechaFin = request.POST['fechaFin']
            fase.save()
            messages.success(request, 'Fase modificada con exito')
            return HttpResponseRedirect(
                '/ss/proyecto/' + str(idProyect) + '/fase/')
    return render(request, 'fasemodificar.html', {'proyecto': idProyect,
                                                  'fase': fase})


def baja_fase(request, idProyect, idFase):
    """
    Vista para realizar la baja de una fase
    :param idProyect: pk del proyecto sobre el cual se esta trabajando
    :param idFase: pk de la fase que se quiere dar de baja
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyect)
        fase = Fase.objects.get(pk=idFase)
        if fase.estado != 'Pendiente':
            return render(request, 'fasebaja.html',
                          {'alerta': 'No se puede suprimir la fase: '
                                     'se encuentra activa',
                           'proyecto': idProyect})
        elif TipoDeItem.objects.filter(fase=fase).__len__() > 0:
            return render(request, 'fasebaja.html',
                          {'alerta': 'No se puede suprimir la fase: '
                                     'contiene Tipos de Items Asociados.',
                           'proyecto': idProyect})
        else:
            fase.delete()
            fases = Fase.objects.filter(proyecto=proyecto).order_by(
                'posicionFase')
            posicion = 1
            for fas in fases:
                fas.posicionFase == posicion
                fas.save()
                posicion += 1
            proyecto.nroFases = posicion - 1
            proyecto.save()
        print 'Hola'
    return HttpResponseRedirect('/ss/proyecto/' + str(idProyect) + '/fase/')


def buscar_fase(request, idProyect):
    """
    Vista para realizar la busqueda de fases
    :param idProyect: codigo del proyecto del cual se van a administrar sus
    fases.
    """
    fases = []
    if request.method == 'POST':
        form = BusquedaFasesForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['columna'] == '1':
                """
                Si el patron a utilizar es el nombre
                """
                fases = Fase.objects.filter(
                    nombre=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '2':
                """
                Si el patron a utilizar es el estado de la fase
                """
                fases = Fase.objects.filter(
                    estado=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de inicio de la fase
                """
                fases = Fase.objects.filter(
                    fechaInicio=form.cleaned_data['busqueda'])
            if form.cleaned_data['columna'] == '3':
                """
                Si el patron a utilizar es la fecha de fin de la fase
                """
                fases = Fase.objects.filter(
                    fechaFin=form.cleaned_data['busqueda'])
    return render(request, 'administrarfases.html',
                  {'proyecto': Proyecto.objects.get(pk=idProyect),
                   'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases que coincidan '
                            'con el patron de busqueda'})

