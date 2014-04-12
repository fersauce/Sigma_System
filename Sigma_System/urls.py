from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^login/$', 'Sigma_System.views.iniciarsesion', name='login'),
    url(r'^inicio/$', 'Sigma_System.views.inicio', name='inicio'),
    url(r'^finalizar/$', 'Sigma_System.views.cerrarsesion', name='finalizar'),
    url(r'^adm_u/$', 'Sigma_System.views.adm_usuario', name='adm_u'),
    url(r'^adm_u_altas/$', 'Sigma_System.views.alta_usuario', name='adm_u_altas'),
)