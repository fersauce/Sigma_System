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
