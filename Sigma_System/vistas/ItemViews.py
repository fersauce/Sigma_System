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
def administrarItem(request):
    its=Item.objects.all()
    return render(request,'AdministrarItem.html', {'items':its})


@login_required(login_url='/login/')
def altaItem(request):
    its=Item.objects.all()
    if request.method == 'POST':
        ti=TipoDeItem.objects.get(id=1)
        name=request.POST['nombre']
        versionA=request.POST['vers']
        compl=request.POST['complejidad']
        pri=request.POST['prior']
        est=request.POST['estado']
        Item.objects.create(tipoItems=ti,version=versionA,complejidad=compl,prioridad=pri,estado=est)
        messages.success(request, 'El item "'+name+'" ha sido creado con exito')

    else:
        return render(request, 'AltaItems.html',)

    return render(request,'AdministrarItem.html', {'items':its})


@login_required(login_url='/login/')
def modificar_item(request, it):
    """
    vista utilizada para dar de baja a un usuario, baja logica
    """
    user = User.objects.get(id=us)
    #direccion = '/ss/adm_u/?page='+request.session['pag_actual']
    if request.method == 'POST':
        user.usuario.direccion = request.POST['direccion']
        user.usuario.tel = request.POST['tel']
        user.usuario.save()
        nombre = user.username
        messages.info(request, 'usuario: '+nombre+', modificado correctamente')
    else:
        return render(request, 'modificarUsuario.html', {'user': user})
    return HttpResponseRedirect('/ss/adm_u/')