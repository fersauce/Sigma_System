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
    print("ruthi")
    print(fase.nombre)
    print tis.first().__getattribute__('nombre')
    if request.method == 'POST':
        ti = TipoDeItem.objects.get(id=request.POST['tipo'])

        name = request.POST['nombre']
        versionA = 1
        compl = request.POST['complejidad']
        pri = request.POST['prior']
        est = "activo"
        Item.objects.create(
            tipoItems=ti,
            nombre=name,
            version=versionA,
            complejidad=compl,
            prioridad=pri,
            estado=est
        )
        messages.success(request,
                         'El item "' + name + '" ha sido creado con exito')

    else:
        return render(request, 'AltaItems.html',
                      {'tipos': tis, 'fase': idFase})

    return render(request, 'AdministrarItem.html', {'items': its, 'fase': idFase})


@login_required(login_url='/login/')
def modificar_item(request, it):
    """
    vista utilizada para modificar un item
    """

    its = Item.objects.get(id=it)
    if request.method == 'POST':
        print(it)
        its.complejidad = request.POST['complejidad']
        its.prioridad = request.POST['prior']
        #its.version=request.POST['version']
        vers = its.version + 1
        its.version = vers
        its.estado = request.POST['estado']

        its.save()
        messages.info(request, 'Item modificado correctamente')
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
    its.estado = "baja"

    its.save()
    messages.error(request, 'El item  ha sido eliminado')
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
    its.save()
    messages.success(request, 'El item  ha sido revivido')
    return HttpResponseRedirect('/ss/adm_i_rev/'+str(its.tipoItems.fase.pk))
