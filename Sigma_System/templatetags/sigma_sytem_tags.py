from django import template
from Sigma_System.models import UsuariosXProyecto
register = template.Library()


@register.filter
def lider(value):
    usuarioXproyecto = UsuariosXProyecto.Objects.get(proyecto=value, lider=True)
    usuario = usuarioXproyecto.usuario
    nombre = usuario.user.username
    return nombre