from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from Sigma_System.models import TipoDeItem, AtribTipoDeItem, Atributo, Item


def administrarAtributos(request, idTI):
    """
    Vista que se encarga de mostrar el panel de administracion de atributos de
    un tipo de item determinado
    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo

    @type idTI: unicode.
    @param idTI: Contiene el id del Tipo de Item asociado a los atributos con
    los que se trabajara aqui.

    @rtype django.shortcuts.render
    @return: AdministrarAtributos.html, pagina en la cual se trabaja con
    los atributos del Tipo de Item.

    @author: Fernando Saucedo
    """
    permisos = request.session['permisos']
    tipoItem = TipoDeItem.objects.get(pk=idTI)
    listaAtributos = AtribTipoDeItem.objects.filter(tipoDeItem=tipoItem)
    return render(request, 'AdministrarAtributos.html',
                  {'atrib_list': listaAtributos, 'ti_asoc': tipoItem, 'permisos': permisos})


def altaAtributo(request, idTI):
    tipoItem = TipoDeItem.objects.get(pk=idTI)
    listaAtributos = AtribTipoDeItem.objects.filter(tipoDeItem=tipoItem)
    tipos = Atributo.objects.all()
    if request.method == 'POST':
        atrib = Atributo.objects.get(pk=request.POST['select'])
        for atributo in listaAtributos:
            if atributo.nombre == request.POST['nombre']:
                messages.error(request, 'Nombre repetido')
                return render(request, 'atributoalta.html',
                              {'atrib_list': listaAtributos,
                               'ti_asoc': tipoItem, 'tipos': tipos})
        AtribTipoDeItem.objects.create(
            tipoDeItem=tipoItem,
            atributos=atrib,
            nombre=request.POST['nombre']
        )
        messages.success(request, 'Atributo creado con exito')
        return HttpResponseRedirect(
            '/ss/proyecto/fase/tipoItem/' + str(idTI) + '/atributo/')

    return render(request, 'atributoalta.html',
                  {'atrib_list': listaAtributos, 'ti_asoc': tipoItem,
                   'tipos': tipos})


def modificarAtributo(request, idTI, idAtributo):
    """
    Vista que se encarga de mostrar el panel de administracion de atributos de
    un tipo de item determinado
    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo

    @type idTI: unicode.
    @param idTI: Contiene el id del Tipo de Item asociado a los atributos con
    los que se trabajara aqui.

    @type idAtributo: unicode.
    @param idAtributo: Contiene el id del Atributo que se quiere dar de baja.

    @rtype django.shortcuts.render
    @return: AdministrarAtributos.html, pagina en la cual se trabaja con
    los atributos del Tipo de Item.

    @author: Fernando Saucedo
    """
    tipoItem = TipoDeItem.objects.get(pk=idTI)
    listaAtributos = AtribTipoDeItem.objects.filter(tipoDeItem=tipoItem)
    atributo = AtribTipoDeItem.objects.get(pk=idAtributo)
    tipos = Atributo.objects.all()
    for atrib in listaAtributos:
        print atrib.nombre
    if request.method == 'POST':
        print 'hola'
        return HttpResponseRedirect(
            '/ss/proyecto/fase/tipoItem/' + str(idTI) + '/atributo/')
    return render(request, 'atributomodificar.html', {'ti_asoc': tipoItem,
                   'tipos': tipos, 'atrib': atributo})

def bajaAtributo(request, idTI, idAtributo):
    """
    Vista que se encarga de mostrar el panel de administracion de atributos de
    un tipo de item determinado
    @type request: django.http.HttpRequest.
    @param request: Contiene la informacion sobre la solicitud de la pagina
    que lo llamo

    @type idTI: unicode.
    @param idTI: Contiene el id del Tipo de Item asociado a los atributos con
    los que se trabajara aqui.

    @type idAtributo: unicode.
    @param idAtributo: Contiene el id del Atributo que se quiere dar de baja.

    @rtype django.shortcuts.render
    @return: AdministrarAtributos.html, pagina en la cual se trabaja con
    los atributos del Tipo de Item.

    @author: Fernando Saucedo
    """
    tipoItem = TipoDeItem.objects.get(pk=idTI)
    listaAtributos = AtribTipoDeItem.objects.filter(tipoDeItem=tipoItem)
    atributo = AtribTipoDeItem.objects.get(pk=idAtributo)
    if request.method == 'GET':
        print 1
        itemsInstanciados = Item.objects.filter(tipoItems=tipoItem)
        if itemsInstanciados.__len__() > 0:
            print 2
            messages.error(request, 'No se puede suprimir este atributo, ya'
                                    'se encuentra instanciado')
            return administrarAtributos(request, idTI)
        try:
            print 3
            mensaje = atributo.nombre
            atributo.delete()
            messages.success(request, 'Atributo ' + str(mensaje) + ' eliminado')
            print 4
        except Exception as error:
            print 5
            messages.error(request, 'Ha ocurrido un error en el sistema, el '
                                    'atributo no ha podido ser eliminado')
            print error.message
            print 6
            return administrarAtributos(request, idTI)
    print 7
    return administrarAtributos(request, idTI)
    pass

