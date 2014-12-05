from django.core.urlresolvers import reverse

__author__ = 'ruth'
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
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/login/')
def administrarItem(request, idFase):
    fase = Fase.objects.get(id=idFase)
    item_baja = Item.objects.filter(tipoItems__fase=fase, estado='baja')
    request.session['fase'] = idFase
    fs = Fase.objects.get(pk=idFase)
    nameFa = fs.nombre
    proy = fs.proyecto
    permisos = request.session['permisos']
    its = Item.objects.filter(tipoItems__fase=fs).exclude(estado='baja')
    return render(request, 'AdministrarItem.html',
                  {'items': its, 'fase': fs,
                   'username': request.user.username,
                   'proy': proy, 'permisos':permisos,
                   'nomb': nameFa, 'item_baja': item_baja})


@login_required(login_url='/login/')
def altaItem(request, idFase, opcion):
    """
    vista utilizada para crear un item
    """
    print "entro en alta item"
    print opcion
    print "------------------"
    print "el id fase es " + idFase
    fase = Fase.objects.get(pk=idFase)
    items_ant = []
    if opcion == '0':
        listaitems1 = Item.objects.filter(tipoItems__fase=fase, estado='aprobado')
        listaitems2 = Item.objects.filter(tipoItems__fase=fase, estado='bloqueado')
        listaitems = listaitems1 | listaitems2
        listaitems = Item.objects.filter(tipoItems__fase=fase).exclude(estado='baja')
        items_ant = get_antecesores(idFase)
    else:
        pos = fase.posicionFase-1
        #definir una funcion para que listaitems reciba items finales en linea base de la fase anterior
        #por ahora recibe todos los items
        fase = Fase.objects.get(proyecto=fase.proyecto, posicionFase=pos)
        #if fase.estado == 'Pendiente':
        #    fase.estado = 'Iniciado'
        #    fase.fechaInicio = datetime.datetime.now()
        #    fase.save()
        #    messages.success(request, 'Fase '+fase.nombre+' iniciada.')
        li = Items_x_LBase.objects.filter(lb__fase=fase, item_final=True)
        listaitems = []
        for l in li:
            listaitems.append(l.item)
        #listaitems = Item.objects.filter(tipoItems__fase__proyecto=fase.proyecto,
        #                                 tipoItems__fase__posicionFase=pos,
        #                                 estado='aprobado')
    its = Item.objects.exclude(estado='baja')
    tis = TipoDeItem.objects.filter(fase=Fase.objects.get(pk=idFase))
    if tis:
        print "no vacio"
    else:
        print "tipo de items vacio"
    print(fase.nombre)
    if request.method == 'POST':
        try:
            ti = TipoDeItem.objects.get(id=request.POST['tipo'])
            name = request.POST['nombre']
            versionA = 1
            compl = request.POST['complejidad']
            pri = request.POST['prior']
            est = "activo"
            id_rel = int(request.POST['i_padre'])
            if id_rel == 0:
                id_rel = int(request.POST['i_ant'])
            itt = Item.objects.create(
                tipoItems=ti,
                nombre=name,
                version=versionA,
                complejidad=compl,
                prioridad=pri,
                estado=est,
                item_padre=id_rel
            )
            #guardarHistorial(its,verAct,verAnt,cod,valorActual,valorAnterior,descrip):
            guardarHistorial(itt,1,0,'a',0,0,'alta')

            #lgkgka
            tipo=itt.tipoItems
            print('nombre del tipo del item '+tipo.nombre)

            idTI=tipo.id
            print('id del tipo de item',tipo.id)
            listaDeAtributos=AtribTipoDeItem.objects.filter(tipoDeItem=idTI)

            for lA in listaDeAtributos:
                print(' nombre del atributo '+ lA.nombre)
                ItemAtributosTipoI.objects.create(
                    item=itt,
                    tipoItemAtrib = lA,
                    valor_atrib = " "
                )


            losItems=ItemAtributosTipoI.objects.filter(item=itt)
            for at in losItems:
                print(at.item.id)

            #,glflas


            messages.success(request,
                             'El item "' + name + '" ha sido creado con exito')
        except Exception:
            messages.error(request, 'Ocurrio un error.')
    else:
        return render(request, 'AltaItems.html',
                      {'tipos': tis,
                       'idfase': idFase,
                       'nombreFase': fase.nombre,
                       'opcion': int(opcion),
                       'listaitems': listaitems,
                       'items_ant': items_ant,
                       'proyectos': fase.proyecto})
    return HttpResponseRedirect(reverse('sigma:adm_i', args=[idFase]))


def get_antecesores(idfase):
    fase = Fase.objects.get(id=idfase)
    lista = []
    if fase.posicionFase == 1:
        return lista
    else:
        pos = fase.posicionFase-1
        fase_ant = Fase.objects.get(proyecto=fase.proyecto, posicionFase=pos)
        i_x_lb = Items_x_LBase.objects.filter(lb__fase=fase_ant)
        for i in i_x_lb:
            lista.append(i.item)
    return lista


def aprobar_desaprobar_item(request, idFase, idItem, opcion):
    item = Item.objects.get(id=idItem)
    fase = Fase.objects.get(id=idFase)
    if item.estado not in ['bloqueado', 'revision']:
        if opcion == '0':
            if item.estado != 'aprobado':
                if item.item_padre != 0:
                    padre = Item.objects.get(id=item.item_padre)
                    if padre.estado in ['aprobado', 'bloqueado']:
                        item.estado = 'aprobado'
                        item.save()
                        messages.success(request, 'El item "' + item.nombre + '" ha sido aprobado')
                    else:
                        messages.error(request, 'El item "' + item.nombre +
                                                '" no puede ser aprobado, el padre del item debe estar '
                                                'aprobado para dar lugar a la operacion')
                else:
                    if fase.posicionFase == 1:
                        item.estado = 'aprobado'
                        item.save()
                        messages.success(request, 'El item "' + item.nombre + '" ha sido aprobado')
                    else:
                        messages.error(request, 'El item "' + item.nombre +
                                                    '" no puede ser aprobado, este item necesita una relacion '
                                                    'con un padre en estado aprobado o con un antecesor para dar '
                                                    'lugar a la operacion')
            else:
                messages.info(request, 'El item "' + item.nombre + '" ya esta aprobado')
        else:
            if item.estado != 'activo':
                items = Item.objects.filter(item_padre=item.id,
                                            tipoItems__fase=fase).exclude(estado='baja')
                ban = False
                if items:
                    for i in items:
                        if i.estado != 'activo':
                            ban = True
                            break
                    if ban:
                        messages.error(request, 'El item "' + item.nombre +
                                            '" no puede ser desaprobado, desapruebe el/los item/s hijo/s'
                                            ' antes de desaprobar este item')
                    else:
                        item.estado = 'activo'
                        item.save()
                        messages.success(request, 'El item "' + item.nombre + '" ha sido desaprobado')
                else:
                    item.estado = 'activo'
                    item.save()
                    messages.success(request, 'El item "' + item.nombre + '" ha sido desaprobado')
            else:
                messages.info(request, 'El item "' + item.nombre + '" ya esta activo')
    else:
        messages.error(request, 'No se puede modificar el estado de un item en linea base')
    return HttpResponseRedirect(reverse('sigma:adm_i', args=[idFase]))


@login_required(login_url='/login/')
def modificar_item(request, it):
    """
    vista utilizada para modificar un item
    donde el parametro it es el id del item
    """

    its = Item.objects.get(id=it)
    losItems=ItemAtributosTipoI.objects.filter(item=its)
    print("entro en modificar")
#lgkgka
    tipo=its.tipoItems
    print('nombre del tipo del item '+tipo.nombre)

    idTI=tipo.id
    print('id del tipo de item',tipo.id)
    listaDeAtributos=AtribTipoDeItem.objects.filter(tipoDeItem=idTI)

    for lA in listaDeAtributos:
        print(' nombre del atributo '+ lA.nombre)
        """ItemAtributosTipoI.objects.create(
            item=itt,
            tipoItemAtrib = lA,
            valor_atrib = " "
        )"""

    losItems=ItemAtributosTipoI.objects.filter(item=its)

    if request.method == 'POST':
        nAct = its.nombre
        comAct = its.complejidad
        priAct = its.prioridad
        vAct = its.version
        estAct = its.estado
        nNuevo = request.POST['nombre']
        comNuevo = request.POST['complejidad']
        priNuevo = request.POST['prior']
       # estNuevo = request.POST['estado']
        listaDeIndices=[]
        listaDeAtributosDelForm=[]
        for li in losItems:
            index='def_'+li.tipoItemAtrib.nombre.__str__()
            listaDeIndices.append(index)

        for i in listaDeIndices:
            listaDeAtributosDelForm.append(request.POST[i])

        print "nombre", nNuevo
        print "complejidad", comNuevo
        print "prioridad", priNuevo
       # print "estado", estNuevo
        historias=Historial.objects.filter(item=its)
        ultimaVersion=int(its.version)+1
        mayor=historias.order_by('-nro_version_act')
        ultimaVersion=mayor[0].nro_version_act
        print mayor[0].nro_version_act
        """
        for h in historias:
            vh=int(h.nro_version_act)
            va=int(its.version)
            if vh > va:
                if vh>=mayor:
                    print 'version en el historial, buscando el mayor ',vh,' es mayor que ',va
                    ""vh=vh*(-1)
                    h.nro_version_act=vh
                    deReversion=1"
                    ultimaVersion=vh+1
                    """


        its.nombre = request.POST['nombre']
        its.complejidad = request.POST['complejidad']
        its.prioridad = request.POST['prior']

        vers = ultimaVersion+1
        vNuevo = vers
        its.version = vers
       # its.estado = request.POST['estado']

        its.save()
        """ modificar los atributos del tipo de item """
        for i in range(listaDeAtributosDelForm.__len__()):
            print 'en la tabla ',losItems[i].valor_atrib
            print 'en el form ',listaDeAtributosDelForm[i]
            if losItems[i].valor_atrib == listaDeAtributosDelForm[i]:
                print "son iguales los atributos"
            else:
                print "no son iguales los atibutos del item"
                #guardarHistorial(its,vNuevo,vAct,'m',nNuevo,nAct,'nombre')
                print 'lo que se va a guardar en el historial'
                print 'valor anterior',losItems[i].valor_atrib,'valor actual',listaDeAtributosDelForm[i],'nombre del campo',listaDeIndices[i]

                guardarHistorial(its,vNuevo,vAct,'m',listaDeAtributosDelForm[i],losItems[i].valor_atrib,losItems[i].id)
                losItems[i].valor_atrib=listaDeAtributosDelForm[i]
                print(losItems[i].valor_atrib)
                losItems[i].save()
                print 'id del atributo: ',losItems[i].id




        messages.info(request, 'Item modificado correctamente')

        if nAct != nNuevo:
            print("entro en el if de nombre")
            #guardarHistorial(its,vNuevo,vAct,'m',nNuevo,nAct,'nombre')
            guardarHistorial(its,vNuevo,vAct,'m',nNuevo,nAct,'nombre')

        if comAct == int(comNuevo):
            print("entro en el if de complejidad")
        else:
             #guardarHistorial(its,vNuevo,vAct,'m',nNuevo,nAct,'nombre')
            guardarHistorial(its,vNuevo,vAct,'m',comNuevo,comAct,'complejidad')

        if priAct == int(priNuevo):
            print("entro en el if de pri")
        else:
            guardarHistorial(its,vNuevo,vAct,'m',priNuevo,priAct,'prioridad')
    else:
        return render(request, 'ModificarItem.html', {'item': its, 'username': request.user.username,'atributos':losItems})
    return HttpResponseRedirect('/ss/adm_i/' + str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def baja_item(request, it):
    """
    vista utilizada para dar de baja un item, baja logica
    donde el parametro it es el id del item a dar de baja
    """
    #user = User.objects.get(id=us)

    its = Item.objects.get(id=it)
    estAnt = its.estado
    its.estado = "baja"
    verActual = its.version
    nVersion = verActual + 1
    its.version = nVersion

    its.save()
    messages.error(request, 'El item  ha sido eliminado')
    #guardarHistorial(its,verAct,verAnt,cod,valorActual,valorAnterior,descrip):
    guardarHistorial(its,nVersion,verActual,'b','baja',estAnt,'baja')
    """
    Historial.objects.create(
        item=its,
        nro_version_act=nVersion,
        nro_version_ant=verActual,
        cod_mod="b",
        valor_act="baja",
        valor_ant=estAnt,
        descripcion="baja",
        fecha_mod=datetime.datetime.now()
    )
    """
    return HttpResponseRedirect('/ss/adm_i/' + str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def revivir_item(request, idFase):
    """
    vista utilizada para mostrar los items a ser revividos

    """
    request.session['fase'] = idFase

    fs = Fase.objects.get(pk=idFase)
    nameFa = fs.nombre
    its = Item.objects.filter(estado='baja',tipoItems__fase=fs)
    proyecto=fs.proyecto

    return render(request, 'RevivirItem.html',
                  {'items': its, 'idFase': idFase,
                   'nomb': nameFa, 'username': request.user.username,
                   'proyecto':proyecto,'permisos':request.session['permisos']})


@login_required(login_url='/login/')
def revivir(request, it):
    """
    vista utilizada para revivir un item eliminado
    donde el parametro it es el id del item a revivir
    """
    #user = User.objects.get(id=us)
    its = Item.objects.get(id=it)
    its.estado = "activo"
    verActual = its.version
    verNuevo = verActual + 1
    its.version = verNuevo
    its.save()
    messages.success(request, 'El item  ha sido revivido')

    Historial.objects.create(
        item=its,
        nro_version_act=verNuevo,
        nro_version_ant=verActual,
        cod_mod="rev",
        valor_act="activo",
        valor_ant="baja",
        descripcion="revivir",
        fecha_mod=datetime.datetime.now()
    )
    return HttpResponseRedirect('/ss/adm_i_rev/' + str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def revertir(request, idFase):
    """
    vista utilizada para mostrar las versiones del item a reversionar

    """

    itemAux = Item.objects.get(id=idFase)
    tipo = itemAux.tipoItems
    fase = tipo.fase
    nameFa = fase.nombre
    proyecto=fase.proyecto

    idf = fase.pk  # Fase.objects.get(nombre=nameFa)
    histor = Historial.objects.filter(item=idFase)

    hist_aux= []
    h_nv= []
    for h in histor:
        if h.nro_version_act not in h_nv:
            hist_aux.append(h)
        h_nv.append(h.nro_version_act)
    return render(request, 'RevertirItem.html',
                  {'hist': hist_aux, 'idfase': idf, 'nomb': nameFa,
                   'items': itemAux, 'username': request.user.username,
                   'permisos':request.session['permisos'],'proyecto':proyecto})


@login_required(login_url='/login/')
def revertirItem(request, idItem, versionRev, idHis):
    """
    vista utilizada para realizar la reversion del item,
    idItem es el id del item que se va a cambiar
    verisonRev es la version a la que ira nuevamente
    historial.item.all

    """
    its = Item.objects.get(id=idItem)
    versionActual = its.version
    #idPadre= Item.
    #if idPadre > 0:
    print ('id del historial a la version que se quiere ir', int(idHis))

    his2 = Historial.objects.get(id=idHis)
    print ('version actual del item', versionActual)
    print ('version a revertir del item', versionRev)

    his1 = Historial.objects.filter(item=its)
    for h in his1:
        print ('version actual en historial', h.nro_version_act)
        if h.nro_version_act == versionActual:
            idHisFinal = int(h.id)
            print ('id en el historial de la version actual', idHisFinal)

    idHisRev = his2.id
    ultimo = idHisFinal
    indice = ultimo + 1
    print('id historial rever', idHisRev)
    print('id historial ultimo', ultimo)
    print('reversion', int(versionRev))
    print('ver actual', int(versionActual))
    b=0
    b1=0
    if int(versionRev) < int(versionActual):
        print('entro en la reversion es menor a la ver actual')
        for i in range(idHisRev, ultimo+1):
            print('for')
            indice = indice - 1
            print(indice)
            historialAux = Historial.objects.get(id=indice)
            itemAuxiliar = historialAux.item
            idLeido = itemAuxiliar.id
            print 'id leido', idLeido
            print 'idParametro', idItem
            if (int(idLeido) == int(idItem)):
                print('id son iguales')
                if int(historialAux.nro_version_act) > 0:
                    if int(historialAux.nro_version_act) <= int(versionActual):
                        print 'version menor', historialAux.nro_version_act
                        print int(historialAux.nro_version_act)
                        print int(versionRev)
                        if int(historialAux.nro_version_act) == int(versionRev):
                            print('reversion encontrada')
                            #messages.info(request, 'Item reversionado')
                            b=1
                            b1=1
                            if historialAux.cod_mod == 'm':
                                if historialAux.descripcion == 'nombre':
                                    print 'revertir de nombre'

                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.nombre = valorActualEnHistorial
                                    its.version = versionActual+1
                                    #its.save()
                                    guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')

                                if historialAux.descripcion == 'complejidad':
                                    print('reversion a un cambio de complejidad')

                                    print 'revertir de complejidad'

                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.complejidad = valorActualEnHistorial
                                    its.version = versionActual+1
                                    print 'valorActualEnHistorial :', valorActualEnHistorial
                                    print 'its.version :',  its.version
                                   # its.save()
                                    guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')

                                if historialAux.descripcion == 'prioridad':
                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.prioridad = valorActualEnHistorial
                                    its.version = versionActual+1

                                    print 'revertir de prioridad'
                                  #  its.save()
                                    guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')

                                if historialAux.descripcion != 'nombre':
                                    if historialAux.descripcion!='complejidad':
                                        if historialAux.descripcion != 'prioridad':
                                            print('cambio en el valor del atributo de id '+historialAux.descripcion+ ' del tipo del item')
                                            numero=int(historialAux.descripcion)
                                            print(numero)
                                            atributoItem=ItemAtributosTipoI.objects.get(id=historialAux.descripcion)
                                            atributoItem.valor_atrib=historialAux.valor_act
                                            atributoItem.save()
                                            its.version = versionActual+1
                                 #   its.save()
                                    #guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')
                            if versionActual == 1:
                                messages.error(request,
                                               'Item no tiene version anterior, no puede reversionarse')

                            if historialAux.cod_mod == 'b':
                                #messages.info(request, 'Item reversionado')
                                its.estado = 'baja'
                                its.version = versionActual+1
                                #its.save()
                                guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')
                            if historialAux.cod_mod=='a':
                                print 'revertir a alta, la primera version'
                                its.version=1
                                its.estado='activo'
                                messages.info(request, 'Item reversionado')
                                #its.save()

                            if historialAux.cod_mod=='rel':
                               idP= historialAux.valor_act
                               itemPapa=Item.objects.get(id=idP)
                               estadoActualPapa=itemPapa.estado
                               print('entro en reversion de asignar relacion')
                               print('estado del papa', estadoActualPapa)
                               if estadoActualPapa=='baja':
                                   b=0
                                   b1=0
                                   print('estado del papa', estadoActualPapa)
                                   messages.error(request,'Item, no puede reversionarse, el padre ha sido eliminado')
                               else:
                                   valorActualEnHistorial = historialAux.valor_act
                                   valorAnteriorEnHistorial = historialAux.valor_ant
                                   its.item_padre = valorActualEnHistorial
                                   its.version = versionActual+1
                                   #messages.info(request, 'Item reversionado')
                                   print 'revertir de asignar relacion'
                                   #its.save()
                                   guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')

                            if historialAux.cod_mod=='desrel':

                                idP= historialAux.valor_ant

                                print('entro en reversion de desasignar relacion')

                                print('femngiesnrguhn',int(idP))


                                itemPapa=Item.objects.get(id=idP)
                                estadoActualPapa=itemPapa.estado
                                print('estado actual del papa',estadoActualPapa)
                                if estadoActualPapa=='baja':
                                    b=0

                                    messages.error(request,'Item, no puede reversionarse, el padre ha sido eliminado')
                                else:
                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.item_padre = 0
                                    its.version = versionActual+1
                                   #messages.info(request, 'Item reversionado')
                                    print 'revertir de desasignar relacion'
                                   #its.save()
                                    guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion')

                            if historialAux.cod_mod == 'rever':
                                valorActualEnHistorial= historialAux.valor_act
                                valorAnteriorEnHistorial=historialAux.valor_ant
                                its.version=versionActual+1
                                print('revertir a  una version que es una reversion')
                                guardarHistorial(its,its.version,versionActual,'rever',valorActualEnHistorial,valorAnteriorEnHistorial,'reversion a una reversion')

                        else:
                            #cambia los valores en la tabla item

                            print 'entro en el si no'
                            if historialAux.cod_mod == 'm':
                                if historialAux.descripcion == 'nombre':
                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.nombre = valorAnteriorEnHistorial
                                    its.version = versionActual+1
                                    print('entro en nombre')
                                    #its.save()
                                if historialAux.descripcion == 'complejidad':
                                    print('reversion a un cambio de complejidad')
                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.complejidad = valorAnteriorEnHistorial
                                    its.version = versionActual+1
                                    print('entro en com')
                                   # its.save()
                                if historialAux.descripcion == 'prioridad':
                                    valorActualEnHistorial = historialAux.valor_act
                                    valorAnteriorEnHistorial = historialAux.valor_ant
                                    its.prioridad = valorAnteriorEnHistorial
                                    its.version = versionActual+1
                                    print('entro en pri')
                                  #  its.save()
                            if historialAux.cod_mod == 'rel':
                                print('ebtro en el rel2')
                                valorActualEnHistorial = historialAux.valor_act
                                valorAnteriorEnHistorial = historialAux.valor_ant
                                if b1==1:
                                    its.item_padre = valorAnteriorEnHistorial
                                    its.version = versionActual+1
                                 #   its.save()
                                    print('kore')
                            if historialAux.descripcion == 'desasignar relacion':

                                valorActualEnHistorial = historialAux.valor_act
                                valorAnteriorEnHistorial = historialAux.valor_ant
                                its.item_padre = valorAnteriorEnHistorial
                                its.version = versionActual+1
                                print('entro en desrel2')
                                #its.save()
        if b>0 and b1>0:
            its.save()
            messages.info(request, 'Item reversionado')

    if int(versionRev) == int(versionActual):
        messages.error(request,'No puede reversionarse  a una misma version')
    return HttpResponseRedirect('/ss/adm_i/' + str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def historialItem(request, idItem):
    """
    vista utilizada para mostrar el historial del item

    """

    its = Item.objects.get(id=idItem)
    fase = its.tipoItems.fase
    his1 = Historial.objects.filter(item__pk=its.pk)
    for hi in his1:
        print hi.descripcion
    tipo=its.tipoItems
    print('nombre del tipo del item '+tipo.nombre)
    return render(request, 'HistorialItem.html',
                  {'his': his1, 'item': its, 'fase': fase})
    #guardarHistorial(its,vNuevo,vAct,'m', nNuevo,    nAct,' nombre')


def guardarHistorial(its,verAct,verAnt,cod,valorActual,valorAnterior,descrip):


    his=Historial.objects.create(
        item=its,
        nro_version_act=verAct,
        nro_version_ant=verAnt,
        cod_mod=cod,
        valor_act="",
        valor_ant=valorAnterior,
        descripcion=descrip,
        fecha_mod=datetime.datetime.now()
    )
    if cod=='b':
        his.valor_act='baja'

    if cod=='a':

        his.valor_act=0

    if cod== 'm':
        his.valor_act=valorActual

    if cod== 'rel':
        his.valor_act=valorActual

    if cod== 'desrel':
        his.valor_act=valorActual


    if cod== 'rever':
        his.valor_act=valorActual


    his.save()
    return
