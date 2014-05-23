from django import template
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from Sigma_System.models import Fase, Item, UsuariosXProyecto
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
    items = Item.objects.filter(tipoItems__fase=fase, estado='aprobado')
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