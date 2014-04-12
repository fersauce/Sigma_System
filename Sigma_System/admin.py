from django.contrib import admin

# Register your models here.
from Sigma_System.models import *

admin.site.register(Proyecto)
admin.site.register(Fase)
admin.site.register(Permiso)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(UsuarioRol)
admin.site.register(Atributo)
admin.site.register(TipoDeItem)
admin.site.register(AtribTipoDeItem)
admin.site.register(Archivo)
admin.site.register(LBase)
admin.site.register(Item)
admin.site.register(ItemAtributosTipoI)
admin.site.register(TipoModificado)
admin.site.register(Historial)
admin.site.register(Solicitud)
admin.site.register(Comite)
admin.site.register(HistorialLineabase)
