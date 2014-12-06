from random import choice
import string
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
from Sigma_System.decoradores import permisos_requeridos
from Sigma_System.funciones_aux import permisos_disponibles
from django.core.urlresolvers import reverse
from Sigma_System.models import Fase, TipoDeItem, Item
from Sigma_System.vistas.ItemViews import get_antecesores,guardarHistorial


def adm_relacion(request, id_item):
    item = Item.objects.get(id=id_item)
    item_padres = Item.objects.filter(id=item.item_padre)
    id_fase = item.tipoItems.fase.id
    id_proy = item.tipoItems.fase.proyecto.id
    ban=True
    if int(item.item_padre) == 0:
        ban= False
    if item_padres:
        if item_padres[0].estado=='baja':
            ban=False
    item_padres = Item.objects.filter(id=item.item_padre).exclude(estado='baja')
    return render(request, 'AdministrarRelacion.html',
                  {'item': item,
                   'item_padres': item_padres,
                   'id_fase': id_fase,
                   'id_proy': id_proy,
                   'ban':ban})


def asignar_padre(request, id_item):
    print('holi')
    item = Item.objects.get(id=id_item)
    items = Item.objects.filter(tipoItems__fase=item.tipoItems.fase).exclude(id=item.id).exclude(estado='baja')
    return render(request, 'AsignarPadre.html', {'items': items, 'item': item})


def asignar_ant(request, id_item):
    item = Item.objects.get(id=id_item)
    items = get_antecesores(item.tipoItems.fase.id)
    return render(request, 'AsignarPadre.html', {'items': items, 'item': item})


def asignar_final(request, hijo, padre):
    if not verificar_ciclos(Item.objects.get(id=int(hijo)), int(padre)):
        item = Item.objects.get(id=hijo)
        padreAnterior=item.item_padre
        item.item_padre = padre
        version=item.version
        versionNueva=version +1
        item.version=versionNueva
        item.save()
        #guardar en el historial el padre.
        # guardarHistorial(its,versionNueva,versionAnterior,'codigo de la modificacion',valorNuevo,valorAnterior,'descripcion de la modificacion')
        print('el padre es', padre)
        guardarHistorial(item,versionNueva,version,'rel',padre,padreAnterior,'asignar relacion')

        messages.success(request, 'La asignacion ha sido creada con exito')
        return HttpResponseRedirect(reverse('sigma:adm_relacion', args=[hijo]))
    else:
        messages.error(request, 'No se puede asociar debido al ciclo que se crearia')
        return HttpResponseRedirect(reverse('sigma:adm_relacion', args=[hijo]))


def ver_hijos(request, id_item):
    item = Item.objects.get(id=id_item)
    items = Item.objects.filter(item_padre=id_item)
    return render(request, 'VerHijos.html', {'item': item, 'items': items})


def verificar_ciclos(item, iditem):
    hijos = Item.objects.filter(item_padre=item.id)
    c = 0
    if hijos.__len__() == 0:
        return False
    for h in hijos:
        if iditem == h.id:
            return True
        else:
            b = verificar_ciclos(h, iditem)
            if not b:
                c += 1
    if c == hijos.__len__():
        return False
    else:
        return True

def desasignarRelacion(request,idItem, idPadre):
    item=Item.objects.get(id=idItem)
    #itemP=Item.objects.get(id=idPadre)
    #estadoPadre=itemP.estado
    #if estadoPadre = 'baja'
     #   messages('No se puede desasignar ')
    item.item_padre=0
    version=item.version
    versionNueva=version+1
    item.version=versionNueva
    item.save()
    guardarHistorial(item,versionNueva,version,'desrel',0,idPadre,'desasignar relacion')
    messages.success(request, 'Se ha eliminado la relacion con exito')
    return adm_relacion(request,idItem)