from django.conf.urls import patterns
from django.conf.urls import url
from Sigma_System.views import ListaJsonUsuarios


urlpatterns = patterns('',
    url(r'^login/$', 'Sigma_System.views.iniciarsesion', name='login'),
    url(r'^inicio/$', 'Sigma_System.views.inicio', name='inicio'),
    url(r'^finalizar/$', 'Sigma_System.views.cerrarsesion', name='finalizar'),
    url(r'^adm_u/$', 'Sigma_System.views.adm_usuario', name='adm_u'),
    url(r'^adm_u_altas/$', 'Sigma_System.views.alta_usuario', name='adm_u_altas'),
    url(r'^nuevopass/$', 'Sigma_System.views.recuperarPass', name='recu_pass'),
    url(r'^adm_u_baja/(?P<us>\d+)$', 'Sigma_System.views.baja_usuario', name='adm_u_baja'),
    url(r'^adm_u_mod/(?P<us>\d+)/$', 'Sigma_System.views.modificar_usuario', name='adm_u_mod'),
    url(r'^adm_u_bus/$', 'Sigma_System.views.buscar_usuario', name='adm_u_bus'),
    url(r'^adm_u_ver/(?P<us>\d+)$', 'Sigma_System.views.ver_detalle', name='adm_u_ver'),
    url(r'^adm_r/$', 'Sigma_System.views.adm_roles', name='adm_r'),
    url(r'^adm_r_altas/$', 'Sigma_System.views.add_roles', name='adm_r_altas'),
    url(r'^adm_r_mod/(?P<id>\d+)$', 'Sigma_System.views.mod_roles', name='adm_r_mod'),
    url(r'^adm_r_baja/(?P<id>\d+)$', 'Sigma_System.views.del_roles', name='adm_r_baja'),
    url(r'^adm_r_buscar/$', 'Sigma_System.views.buscar_roles', name='adm_r_buscar'),
    url(r'^adm_r_buscar/$', 'Sigma_System.views.buscar_roles', name='adm_r_buscar'),
    url(r'^adm_u_listar/$', ListaJsonUsuarios.as_view(), name='adm_u_listar'),
)