from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^login/$', 'Sigma_System.views.iniciarsesion', name='login'),
    url(r'^inicio/$', 'Sigma_System.views.inicio', name='inicio'),
    url(r'^finalizar/$', 'Sigma_System.views.cerrarsesion', name='finalizar'),
    url(r'^adm_u/$', 'Sigma_System.views.adm_usuario', name='adm_u'),
    url(r'^adm_u_altas/$', 'Sigma_System.views.alta_usuario', name='adm_u_altas'),
    url(r'^nuevopass/$', 'Sigma_System.views.recuperarPass', name='recu_pass'),
    url(r'^adm_u_baja/(?P<us>\d+)$', 'Sigma_System.views.baja_usuario', name='adm_u_baja'),
    url(r'^adm_u_mod/(?P<us>\d+)$', 'Sigma_System.views.modificar_usuario', name='adm_u_mod'),
    url(r'^adm_u_bus/$', 'Sigma_System.views.buscar_usuario', name='adm_u_bus'),
    url(r'^adm_u_ver/(?P<us>\d+)$', 'Sigma_System.views.ver_detalle', name='adm_u_ver'),
)