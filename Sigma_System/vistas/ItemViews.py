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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/login/')
def administrarItem(request, idFase):
    request.session['fase'] = idFase

    fs = Fase.objects.get(pk=idFase)
    nameFa=fs.nombre
    its = Item.objects.exclude(estado='baja')
    return render(request, 'AdministrarItem.html',{'items': its, 'fase': idFase, 'nomb':nameFa})


@login_required(login_url='/login/')
def altaItem(request, idFase):
    """
    vista utilizada para crear un item
    """
    its = Item.objects.exclude(estado='baja')

    tis = TipoDeItem.objects.filter(fase=Fase.objects.get(pk=idFase))
    fase=Fase.objects.get(pk=idFase)
    print(fase.nombre)
    print tis.first().__getattribute__('nombre')
    if request.method == 'POST':
        ti = TipoDeItem.objects.get(id=request.POST['tipo'])

        name = request.POST['nombre']
        versionA = 1
        compl = request.POST['complejidad']
        pri = request.POST['prior']
        est = "activo"
        itt=Item.objects.create(
            tipoItems=ti,
            nombre=name,
            version=versionA,
            complejidad=compl,
            prioridad=pri,
            estado=est
        )
        messages.success(request,
                         'El item "' + name + '" ha sido creado con exito')


        Historial.objects.create(
            item=itt,
            nro_version_act = 1,
            nro_version_ant = 0,
            cod_mod = "a",
            valor_act = 0,
            valor_ant = 0,
            descripcion ="alta",
            fecha_mod = datetime.datetime.now()
        )
    else:
        return render(request, 'AltaItems.html',
                      {'tipos': tis, 'fase': idFase})

    return render(request, 'AdministrarItem.html', {'items': its, 'fase': idFase})


@login_required(login_url='/login/')
def modificar_item(request, it):
    """
    vista utilizada para modificar un item
    donde el parametro it es el id del item
    """

    its = Item.objects.get(id=it)
    if request.method == 'POST':
        print(it)
        nAct=its.nombre
        comAct=its.complejidad
        priAct=its.prioridad
        vAct=its.version
        estAct=its.estado

        nNuevo=request.POST['nombre']
        comNuevo=request.POST['complejidad']
        priNuevo=request.POST['prior']
        estNuevo=request.POST['estado']
        print "nombre",nNuevo
        print "complejidad",comNuevo
        print "prioridad",priNuevo
        print "estado",estNuevo

        its.nombre=request.POST['nombre']
        its.complejidad = request.POST['complejidad']
        its.prioridad = request.POST['prior']

        vers = its.version + 1
        vNuevo=vers
        its.version = vers
        its.estado = request.POST['estado']


        its.save()
        messages.info(request, 'Item modificado correctamente')


        if nAct != nNuevo:
            print("entro en el if de nombre")
            Historial.objects.create(
                item=its,
                nro_version_act = vNuevo,
                nro_version_ant = vAct,
                cod_mod = "m",
                valor_act = nNuevo,
                valor_ant = nAct,
                descripcion = "nombre modificado",
                fecha_mod = datetime.datetime.now()
            )
        print request.POST['complejidad']
        if comAct == int(comNuevo):
            print("entro en el if de complejidad")
            print("complejidad1" , comAct)
            print('complejidad2' ,comNuevo)
        else:
            Historial.objects.create(
                item=its,
                nro_version_act = vNuevo,
                nro_version_ant = vAct,
                cod_mod="m",
                valor_act=comNuevo,
                valor_ant = comAct,
                descripcion = "complejidad modificada",
                fecha_mod = datetime.datetime.now()
            )
        suma=int(priNuevo)+9
        print suma
        if priAct == int(priNuevo):
            print("entro en el if de pri")
        else:
            Historial.objects.create(
                item=its,
                nro_version_act = vNuevo,
                nro_version_ant = vAct,
                cod_mod = "m",
                valor_act = priNuevo,
                valor_ant = priAct,
                descripcion = "prioridad modificada",
                fecha_mod = datetime.datetime.now()
            )
        if estAct != estNuevo:
            print("entro en el if de estado")
            Historial.objects.create(
                item=its,
                nro_version_act = vNuevo,
                nro_version_ant = vAct,
                cod_mod = "m",
                valor_act = estNuevo,
                valor_ant = estAct,
                descripcion = "estado modificado",
                fecha_mod = datetime.datetime.now()
            )

    else:
        return render(request, 'ModificarItem.html', {'item': its})
    return HttpResponseRedirect('/ss/adm_i/'+str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def baja_item(request, it):
    """
    vista utilizada para dar de baja un item, baja logica
    donde el parametro it es el id del item a dar de baja
    """
    #user = User.objects.get(id=us)

    its = Item.objects.get(id=it)
    estAct=its.estado
    its.estado = "baja"
    verActual=its.version
    nVersion=verActual+1
    its.version=nVersion


    its.save()
    messages.error(request, 'El item  ha sido eliminado')

    Historial.objects.create(
        item=its,
        nro_version_act = nVersion,
        nro_version_ant = verActual,
        cod_mod = "b",
        valor_act = "baja",
        valor_ant = estAct,
        descripcion = "baja",
        fecha_mod = datetime.datetime.now()
    )





    return HttpResponseRedirect('/ss/adm_i/'+str(its.tipoItems.fase.pk))


@login_required(login_url='/login/')
def revivir_item(request, idFase):
    """
    vista utilizada para mostrar los items a ser revividos

    """
    request.session['fase'] = idFase

    fs = Fase.objects.get(pk=idFase)
    nameFa=fs.nombre
    its = Item.objects.filter(estado='baja')

    return render(request, 'RevivirItem.html',{'items': its, 'fase': idFase, 'nomb':nameFa})


@login_required(login_url='/login/')
def revivir(request, it):
    """
    vista utilizada para revivir un item eliminado
    donde el parametro it es el id del item a revivir
    """
    #user = User.objects.get(id=us)
    its = Item.objects.get(id=it)
    its.estado = "activo"
    verActual=its.version
    verNuevo=verActual+1
    its.version=verNuevo
    its.save()
    messages.success(request, 'El item  ha sido revivido')

    Historial.objects.create(
        item=its,
        nro_version_act = verNuevo,
        nro_version_ant = verActual,
        cod_mod = "rev",
        valor_act = "activo",
        valor_ant = "baja",
        descripcion = "item revivido",
        fecha_mod = datetime.datetime.now()
    )


    return HttpResponseRedirect('/ss/adm_i_rev/'+str(its.tipoItems.fase.pk))
