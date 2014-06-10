from django.contrib import messages
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import simplejson
import sys
from Sigma_System.models import Item, Archivo


def administrarArchivos(request, idItem):
    item = Item.objects.get(pk=idItem)
    archivos = item.arch_adjuntos.all().filter(activo=True)
    return render(request, 'administrarArchivos.html', {'item':item,
                                                        'archivos': archivos})


def agregarArchivo(request, idItem):
    item = Item.objects.get(pk=idItem)
    if request.is_ajax():
        try:
            c = {}
            c.update(csrf(request))
            print csrf(request)
            enviar = {'token': 'hola'}
            print 'ajax'
            return HttpResponse(simplejson.dumps(enviar),
                                mimetype='application/json')
        except DeprecationWarning:
            print "Solo Warning"
    if request.method == 'POST':
        try:
            archivo = Archivo()
            archivo.archivo_adj = request.FILES['arch']
            archivo.save()
            item.arch_adjuntos.add(archivo)
            item.save()
            messages.success(request, 'Archivo cargado y asociado al item')
        except Exception:
            messages.error(request, 'Ha ocurrido un error, pongase en contacto '
                                    'con el administrador')
            print sys.exc_info()

    return HttpResponseRedirect(reverse('sigma:adm_arch', args=[idItem]))


def eliminarArchivo(request, idItem, idArchivo):
    item = Item.objects.get(pk=idItem)
    archivo = item.arch_adjuntos.get(pk=idArchivo)
    if request.method == 'POST':
        archivo.activo = False
        archivo.save()
        item.save()
    return HttpResponseRedirect(reverse('sigma:adm_arch' ,args=[idItem]))