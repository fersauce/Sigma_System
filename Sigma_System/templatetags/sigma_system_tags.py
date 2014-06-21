from django import template
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from Sigma_System.models import Fase, Item, UsuariosXProyecto, TipoDeItem, Historial, UsuarioRol
register = template.Library()


@register.filter
def lider(value):
    usuarioXproyecto = UsuariosXProyecto.objects.filter(proyecto=value, lider=True)
    if usuarioXproyecto:
        nombre = usuarioXproyecto[0].usuario.user.username
    else:
        nombre = ""
    return nombre


@register.filter
def habilitar_evento(value, arg):
    fase = Fase.objects.get(id=value)
    items = Item.objects.filter(tipoItems__fase=fase, estado='aprobado') | \
            Item.objects.filter(tipoItems__fase=fase, estado='bloqueado')
    if fase.posicionFase == 1:
        if arg == 0:
            # 0: listar padre y default
            return ' href='+reverse('sigma:adm_i_alta', args=(value, 0))
        else:
            return ''
    else:
        if not items:
            if arg == 0:
                # 1: listar solo antecesores
                return ' href =' + reverse('sigma:adm_i_alta', args=(value, 1))
            else:
                return ''
        else:
            if arg == 0:
                return ''
            else:
                cadena = " onclick=\"elegir_relacion()\""
                cadena = format_html(cadena)
                return cadena


@register.filter
def verificar_ti(value):
    fase = Fase.objects.filter(id=value)
    tipo_items = TipoDeItem.objects.filter(fase=fase)
    if not tipo_items:
        return ' disabled'
    else:
        return ''


@register.filter()
def ti_instanciado(value):
    ti = TipoDeItem.objects.get(pk=value)
    item = Item.objects.filter(tipoItems=ti)
    if item:
        return 'disabled'
    else:
        return ''


@register.filter
def verificar_fase(value):
    fase = Fase.objects.get(id=value)
    items1 = Item.objects.filter(tipoItems__fase=fase)
    items2 = Item.objects.filter(tipoItems__fase=fase, estado='bloqueado')
    if fase.estado == 'Cerrado':
        return 'disabled'
    if items1.__len__() == items2.__len__():
        return ''
    else:
        return 'disabled'


@register.filter
def verificar_lb(value):
    fase = Fase.objects.get(id=value)
    items1 = Item.objects.filter(tipoItems__fase=fase)
    items2 = Item.objects.filter(tipoItems__fase=fase, estado='bloqueado')
    if items1.__len__() == items2.__len__():
        return 'disabled'
    else:
        return ''


@register.filter
def divisiblepor(value, arg):
    return (value-1) % arg == 0


@register.filter
def habilitar_add_atrib(value):
    ti = TipoDeItem.objects.get(id=value)
    items = Item.objects.filter(tipoItems=ti)
    if items:
        return True
    else:
        return False


@register.filter
def habilitar_opciones(value):
    item = Item.objects.get(id=value)
    if item.estado != 'activo':
        return 'disabled'
    else:
        return ''


@register.filter
def rol_proy(value, arg):
    u_r = UsuarioRol.objects.filter(usuario=arg, idProyecto=value.id, idFase=0)
    nombre_rol = 'indefinido'
    if u_r:
        nombre_rol = u_r[0].rol.nombre
    return nombre_rol

@register.filter
def rol_fase(value, arg):
    u_r = UsuarioRol.objects.filter(usuario=arg, idProyecto=value.proyecto.id, idFase=value.id)[0]
    return u_r.rol.nombre