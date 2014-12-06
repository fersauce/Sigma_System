from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import *
import simplejson
from Sigma_System.forms import BusquedaFasesForm
from Sigma_System.models import Proyecto, Usuario, Fase, TipoDeItem, LBase, Items_x_LBase, Item, \
    UsuarioRol, UsuariosXProyecto
from Sigma_System.decoradores import permisos_requeridos
from django.contrib.auth.decorators import login_required
from Sigma_System.funciones_aux import permisos_disponibles
import datetime, time


@login_required(login_url='/login/')
def administrar_fases(request, idProyect):
    """
    Vista para acceder a la administracion de fases de un proyecto.
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: codigo del proyecto del cual se van a trabajar.
    """
    request.session['idProyectoActual'] = idProyect
    proyecto = Proyecto.objects.get(pk=idProyect)
    #fases = Fase.objects.filter(proyecto=proyecto).order_by('posicionFase')
    #us_x_proy = UsuariosXProyecto.objects.filter(proyecto=proyecto, usuario=request.user.usuario)
    #idp = idProyect
    #if us_x_proy:
    #    if us_x_proy[0].lider:
    #        idp = '0'

    request.session['permisos'] = permisos_disponibles(request, 1, int(idProyect), 0)
    permisos = request.session['permisos']
    print "/*/*/*/*/*"
    print permisos
    print "/*/*/*/*/*"
    fases = fases_por_usuario(idProyect, request.user)
    return render(request, 'administrarfases.html',
                  {'proyecto': proyecto, 'fases': fases,
                   'form': BusquedaFasesForm(),
                   'vacio': 'No se encontraron fases asociadas a este '
                            'proyecto',
                   'permisos': permisos,
                   'contexto': request.session['contexto']})


def fases_por_usuario(idp, usuario):#, permisos):
    usu_roles = UsuarioRol.objects.filter(usuario=usuario.usuario, idProyecto=idp)
    fases = []
    usu_proyecto = UsuariosXProyecto.objects.filter(usuario=usuario.usuario, proyecto=Proyecto.objects.get(id=idp))
    if usu_proyecto:
        if usu_proyecto[0].lider and usu_proyecto[0].activo:
            return Fase.objects.filter(proyecto=idp).order_by('posicionFase')
    #if 'super_us' in permisos:
    #    return Fase.objects.filter(proyecto=idp).order_by('posicionFase')
    for u_r in usu_roles:
        if u_r.idFase != 0:
            fases.append(Fase.objects.get(id=u_r.idFase))
    return fases


@login_required(login_url='/login/')
@permisos_requeridos(['crear_fa'], 'sigma:adm_fase', 'crear fases', 1)
def alta_fase(request, idProyect):
    """
    Vista para realizar la alta de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: codigo del proyecto del cual se van a trabajar.
    """
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        proyecto = Proyecto.objects.get(pk=idProyect)
        nombre = request.POST['nombre']
        fase = Fase.objects.filter(proyecto=proyecto)
        for fas in fase:
            if fas.nombre == nombre:
                messages.error(request, 'Nombre de fase ya utilizado')
                return render(request, 'fasealta.html',
                              {'proyecto': idProyect})
        estado_aux = 'Pendiente'
        if not fase:
            estado_aux = 'Iniciado'
        Fase.objects.create(
            proyecto=proyecto,
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            posicionFase=Fase.objects.filter(
                proyecto=proyecto).__len__() + 1,
            estado=estado_aux,
            fechaInicio=datetime.datetime.now(),
            fechaFin=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        fases = Fase.objects.filter(proyecto=proyecto)
        if fases and proyecto.estado != "Iniciado":
            proyecto.estado = "Iniciado"
        proyecto.save()
        messages.success(request, 'Fase creada con exito')
        return HttpResponseRedirect(
            '/ss/proyecto/' + str(idProyect) + '/fase/')
    else:
        proyecto = Proyecto.objects.get(pk=idProyect)
        fases = Fase.objects.filter(proyecto=proyecto)
        if fases.__len__() == proyecto.nroFases:
            messages.error(request,
                           'Ya no puede agregar mas fases, ya se encuentran '
                           'todas las fases creadas.')
            return HttpResponseRedirect(
                reverse('sigma:adm_fase', args=[idProyect]))
    return render(request, 'fasealta.html', {'usuarios': usuarios,
                                             'proyecto': idProyect})


@login_required(login_url='/login/')
@permisos_requeridos(['modificar_fa'], 'sigma:adm_fase', 'modificar fases', 1)
def modificar_fase(request, idProyect, idFase):
    """
    Vista para realizar la modificacion de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.
    @type idProyect: Unicode
    @param idProyect: pk del proyecto sobre el cual se esta trabajando.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere modificar.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    fase = Fase.objects.get(pk=idFase)
    proyecto = Proyecto.objects.get(pk=idProyect)
    if request.method == 'POST':
        if fase.nombre == request.POST['nombre'] or Fase.objects.get(nombre=request.POST['nombre']):
            print proyecto.nroFases
            fases = Fase.objects.filter(proyecto=proyecto).exclude(pk=idFase)
            fase.nombre = request.POST['nombre']
            fase.descripcion = request.POST['descripcion']
            fase.save()
            proyecto.fechaInicio = Fase.objects.get(
                proyecto=proyecto,
                posicionFase=1).fechaInicio
            proyecto.fechaFinalizacion = Fase.objects.get(
                proyecto=proyecto,
                posicionFase=proyecto.nroFases).fechaFin
            proyecto.save()
            messages.success(request, 'Fase modificada con exito')
            return HttpResponseRedirect(
                reverse('sigma:adm_fase', args=[idProyect]))
    return render(request, 'fasemodificar.html', {'proyecto': idProyect,
                                                  'fase': fase})


def linea_base(request, idProyecto, idFase):
    item = Item.objects.get(id=34)
    print '==========================='
    print item.nombre
    print '==========================='
    lista = lista_des(item)
    for i in lista:
        print i.nombre, i.id
    lb = LBase.objects.filter(fase=Fase.objects.get(id=idFase)).order_by('id')
    return render(request, 'LineaBase.html', {'id_proy': idProyecto, 'id_fase': idFase, 'lineasbase': lb})


def establecer_linea_base(request, idProyecto, idFase):
    #item_finales devuelve todos los items en estado aprobados
    itemfinales = traer_itemfinales(idFase)
    if request.method == 'POST':
        obs = request.POST['obs']
        lb = LBase.objects.create(obs=obs, fase=Fase.objects.get(id=idFase))
        i_finales = request.POST.getlist('items_finales')
        for i in i_finales:
            item_actual = Item.objects.get(id=i)
            item_actual.estado = 'bloqueado'
            item_actual.save()
            Items_x_LBase.objects.create(lb=lb, item=item_actual, item_final=True)
        '''
            i_padres = traer_items_padre(i_finales, idFase)
            for i in i_padres:
                i.estado = 'bloqueado'
                i.save()
                Items_x_LBase.objects.create(lb=lb, item=i)
        '''
        fase = Fase.objects.get(pk=idFase)
        proyecto = fase.proyecto
        if not proyecto.nroFases == fase.posicionFase:
            faseSig = Fase.objects.get(posicionFase=fase.posicionFase+1, proyecto=proyecto)
            if faseSig.estado == 'Pendiente':
                faseSig.estado = 'Iniciado'
                fase.fechaInicio = datetime.datetime.now()
                faseSig.save()
                messages.success(request, 'Fase '+faseSig.nombre+' iniciada.')
        messages.success(request, 'Se agregaron correctamente los items a la linea base')
        return HttpResponseRedirect(reverse('sigma:adm_fase_lb', args=(idProyecto, idFase)))
    else:
        return render(request, 'AsignarItemxLB.html', {'id_proy': idProyecto, 'id_fase': idFase, 'itemfinales':itemfinales})


def lista_des(item):
    hijos = Item.objects.filter(tipoItems__fase=item.tipoItems.fase,
                                item_padre=item.id, estado='aprobado').order_by('id')
    print '/*/*/*/*/*/*/*/*/*/*/*/*/*/*'
    print 'item padre: ', item.nombre
    for i in hijos:
        print '   item hijos: ', i.nombre
    print '/*/*/*/*/*/*/*/*/*/*/*/*/*/*'
    lista = [item]
    if not hijos:
        return lista
    else:
        for h in hijos:
            lista = lista + lista_des(h)
        return lista


def traer_itemfinales(idFase):
    fase = Fase.objects.get(id=idFase)
    items = Item.objects.filter(tipoItems__fase=fase, estado='aprobado')
    items_finales = []
    if fase.posicionFase == 1:
        for i in items:
            if i.item_padre == 0:
                items_finales.append(i)
            else:
                padre = Item.objects.get(id=i.item_padre)
                if padre.estado == 'bloqueado' or padre.estado == 'revision':
                    items_finales.append(i)
    else:
        for i in items:
            padre = Item.objects.get(id=i.item_padre)
            if padre.estado == 'bloqueado':
                items_finales.append(i)
    listafinal = []
    for i in items_finales:
        listafinal = lista_des(i) + listafinal
    return listafinal


def traer_items_padre(i_finales, idFase):
    fase = Fase.objects.get(id=idFase)
    items_padre = []
    for i in i_finales:
        i_actual = Item.objects.get(id=i)
        while i_actual.item_padre != 0 and i_actual.tipoItems.fase == fase:
            i_actual = Item.objects.get(id=i_actual.item_padre)
            if i_actual not in items_padre:
                items_padre.append(i_actual)
    return items_padre


@login_required(login_url='/login/')
@permisos_requeridos(['eliminar_fa'], 'sigma:adm_fase', 'eliminar fases', 1)
def baja_fase(request, idProyect, idFase):
    """
    Vista para realizar la baja de una fase
    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idProyect: Unicode
    @param idProyect: pk del proyecto sobre el cual se esta trabajando.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere dar de baja.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(pk=idProyect)
        fase = Fase.objects.get(pk=idFase)
        if fase.estado != 'Pendiente':
            messages.error(request,
                           'No se puede suprimir la fase: se encuentra activa')
            return render(request, 'fasebaja.html',
                          {'proyecto': idProyect})
        elif TipoDeItem.objects.filter(fase=fase).__len__() > 0:
            messages.error(request,
                           'No se puede suprimir la fase: contiene Tipos de '
                           'Items Asociados.')
            return render(request, 'fasebaja.html',
                          {'proyecto': idProyect})
        else:
            try:
                fase.delete()
                fases = Fase.objects.filter(proyecto=proyecto).order_by(
                    'posicionFase')
                posicion = 1
                for fas in fases:
                    fas.posicionFase == posicion
                    fas.save()
                    posicion += 1
            except Exception:
                messages.error(request, 'Ha ocurrido un error interno')
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
                #Si el patron a utilizar es la fecha de fin de la fase
                fases = Fase.objects.filter(
                    fechaFin=form.cleaned_data['busqueda'])
    return render(request, 'administrarfases.html',
                  {'proyecto': Proyecto.objects.get(pk=idProyect),
                   'fases': fases,
                   'form': BusquedaFasesForm()})


def intercambiarFase(request, idFase):
    """
    Vista que realiza el intercambio de fases (Esto lo puede realizar solo en
    tiempo de creacion, una vez iniciado el proyecto, esto ya no puede variar)

    @type request: django.http.HttpRequest
    @param request: contiene los datos de la pagina que lo llamo.

    @type idFase: Unicode
    @param idFase: pk de la fase que se quiere cambiar.

    @rtype django.shortcuts.render
    @return: Administrarfase.html
    """
    fase = Fase.objects.get(pk=idFase)
    if request.is_ajax():
        print "Llamada Ajax de intercambiarFase"
        try:
            enviar = []
            for u in Fase.objects.filter(proyecto=fase.proyecto,
                                         estado='Pendiente').exclude(
                    pk=idFase).order_by('posicionFase'):
                enviar.append({'pkFase': u.pk, 'posicion': u.posicionFase,
                               'nombre': u.nombre})
            return HttpResponse(simplejson.dumps(enviar),
                                mimetype='application/json')
        except DeprecationWarning:
            print "Solo es warning"
    opcion = request.GET['posicion']
    faseIntercambiada = Fase.objects.get(pk=opcion)
    try:
        pasador = fase.posicionFase
        fase.posicionFase = faseIntercambiada.posicionFase
        faseIntercambiada.posicionFase = pasador
        fase.save()
        faseIntercambiada.save()
        messages.success(request,
                         'se han intercambiado satisfactoriamente la fase ' +
                         fase.nombre + ' con la fase ' + faseIntercambiada.nombre)
    except Exception:
        messages.error(request, 'Solo es precaucion')
    return HttpResponseRedirect(
        reverse('sigma:adm_fase', args=[fase.proyecto.pk]))


def administrarUsuariosAsociadosFase(request, idProyect, idFase):
    proyecto = Proyecto.objects.get(id=idProyect)
    fase = Fase.objects.get(id=idFase)
    usu_rol = UsuarioRol.objects.filter(idProyecto=idProyect, idFase=idFase)
    usuarios = []
    for u_r in usu_rol:
        usuarios.append(u_r.usuario)
    return render(request, 'AdministradorUsuarioFase.html', {'usuarios': usuarios,
                                                   'proyecto': proyecto,
                                                   'fase': fase,
                                                   'permisos': request.session['permisos']})


def asignarUsuarioFase(request, idProyect, idFase):
    """
    Vista que asigna los usuarios a un proyecto determinado.

    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo.

    @type idProyect: Unicode
    @param idProyect: Contiene el id del proyecto que se va a asociar/desasociar
    usuarios.

    @rtype django.shortcuts.render
    @return: AdministrarProyecto.html, pagina en la cual se trabaja con los
    proyectos.
    """
    proyecto = Proyecto.objects.get(pk=idProyect)
    fase = Fase.objects.get(id=idFase)
    usu_rol = UsuarioRol.objects.filter(idProyecto=idProyect, idFase=0)
    usuarios3 = []
    for u_r in usu_rol:
        usuarios3.append(u_r.usuario)


    usu_rol2 = UsuarioRol.objects.filter(idProyecto=idProyect, idFase=idFase)
    usuarios2 = []
    for u_r in usu_rol2:
        usuarios2.append(u_r.usuario)

    usuarios = []

    for u in usuarios3:
        if u not in usuarios2:
            usuarios.append(u)

    if request.method == 'POST':
        print 'entra en post'
        usuariosfase = request.POST.getlist('usuariosAsig')
        print '/*-85*/-65*-/*-/-*/'
        for u in usuariosfase:
            usuario = Usuario.objects.get(id=u)
            rol = UsuarioRol.objects.filter(usuario=usuario, idProyecto=idProyect)[0].rol
            try:
                UsuarioRol.objects.create(
                        rol=rol,
                        usuario=usuario,
                        idProyecto=idProyect,
                        idFase=idFase)
                messages.success(request,
                                 'El usuario ' +
                                 usuario.user.username
                                 + ' ha sido asignado a la fase ' +
                                 fase.nombre)
            except Exception:
                messages.error(request,
                               'Ha ocurrido un erro interno, favor'
                               ' contacte al administrador')
        return HttpResponseRedirect(reverse('sigma:adm_fase_usu', args=(idProyect, idFase)))
    return render(request, 'AsignarUsuarioFase.html', {'usuarios': usuarios,
                                                   'proyecto': proyecto,
                                                   'fase': fase,
                                                   'permisos': request.session['permisos']})


def desasignarUsuarioFase(request, idProyect, idFase, idUser):
    fase = Fase.objects.get(id=idFase)
    usuario = Usuario.objects.get(id=idUser)
    uxr = UsuarioRol.objects.filter(usuario=usuario, idProyecto=idProyect, idFase=idFase)[0]
    uxr.delete()
    messages.success(request, 'El usuario ' +
                              usuario.user.username
                              + ' ha sido desasignado de la fase ' +
                              fase.nombre)
    return HttpResponseRedirect(reverse('sigma:adm_fase_usu', args=(idProyect, idFase)))




def finalizar_fase(request, idp, idf):
        fase = Fase.objects.get(id=idf)
        fase.estado = 'Cerrado'
        fase.save()
        messages.success(request, 'Se ha finalizado correctamente la fase "'+fase.nombre+'"')
        return HttpResponseRedirect(reverse('sigma:adm_fase', args=[idp]))