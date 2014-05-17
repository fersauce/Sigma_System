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


def adm_relacion(request, id_item):
    item = Item.objects.get(id=id_item)
    item_padres = Item.objects.filter(id=item.item_padre)
    id_fase = item.tipoItems.fase.id
    id_proy = item.tipoItems.fase.proyecto.id
    return render(request, 'AdministrarRelacion.html',
                  {'item': item,
                   'item_padres': item_padres,
                   'id_fase': id_fase,
                   'id_proy': id_proy})


def asignar_padre(request, id_item):
    item = Item.objects.get(id=id_item)
    items = Item.objects.filter(fase=item.fase).exclude(id=item.id)
    return render(request, 'AsignarPadre.html', {'items': items, 'item': item})


def asignar_final(request, hijo, padre):
    print verificar_ciclos(Item.objects.get(id=1), 9)
    if not verificar_ciclos(Item.objects.get(id=int(hijo)), int(padre)):
        item = Item.objects.get(id=hijo)
        item.item_padre = padre
        item.save()
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