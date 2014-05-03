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
    url(r'^adm_u_mod/(?P<us>\d+)/$', 'Sigma_System.views.modificar_usuario', name='adm_u_mod'),
    url(r'^adm_u_bus/$', 'Sigma_System.views.buscar_usuario', name='adm_u_bus'),
    url(r'^adm_u_ver/(?P<us>\d+)$', 'Sigma_System.views.ver_detalle', name='adm_u_ver'),
    url(r'^adm_u_asig_rol/(?P<id>\d+)$', 'Sigma_System.views.asignar_roles', name='adm_u_asig_rol'),
    url(r'^adm_u_desasig_rol/(?P<id>\d+)$', 'Sigma_System.views.desasignar_roles', name='adm_u_desasig_rol'),
    url(r'^rol/$', 'Sigma_System.vistas.RolPermisosViews.adm_roles',
        name='adm_r'),
    url(r'^rol/nuevo/$', 'Sigma_System.vistas.RolPermisosViews.add_roles',
        name='adm_r_altas'),
    url(r'^rol/modificar/(?P<id>\d+)$', 'Sigma_System.vistas.RolPermisosViews.mod_roles',
        name='adm_r_mod'),
    url(r'^rol/eliminar/(?P<id>\d+)$', 'Sigma_System.vistas.RolPermisosViews.del_roles',
        name='adm_r_baja'),
    url(r'^rol/buscar/$', 'Sigma_System.vistas.RolPermisosViews.buscar_roles',
        name='adm_r_buscar'),
    url(r'^proyecto/$',
        'Sigma_System.vistas.ProyectoViews.administrar_proyecto',
        name='adm_proy'),
    url(r'^proyecto/nuevo/$',
       'Sigma_System.vistas.ProyectoViews.alta_proyecto',
       name='adm_proy_alta'),
    url(r'^proyecto/modificar/(?P<idProyecto>\d+)$',
       'Sigma_System.vistas.ProyectoViews.modificar_proyecto',
       name='adm_proy_mod'),
    url(r'^proyecto/eliminar/(?P<idProyecto>\d+)$',
       'Sigma_System.vistas.ProyectoViews.baja_proyecto',
       name='adm_proy_baja'),
    url(r'^proyecto/buscar/$',
       'Sigma_System.vistas.ProyectoViews.buscar_proyecto',
       name='adm_proy_busq'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/$',
       'Sigma_System.vistas.FaseViews.administrar_fases',
       name='adm_fase'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/buscar/$',
       'Sigma_System.vistas.FaseViews.buscar_fase',
       name='adm_fase_busq'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/alta',
       'Sigma_System.vistas.FaseViews.alta_fase',
       name='adm_fase_alta'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/modificar/(?P<idFase>\d+)',
       'Sigma_System.vistas.FaseViews.modificar_fase',
       name='adm_fase_mod'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/baja/(?P<idFase>\d+)',
       'Sigma_System.vistas.FaseViews.baja_fase',
       name='adm_fase_baja'),
    )