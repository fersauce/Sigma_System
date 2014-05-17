from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^login/$', 'Sigma_System.views.iniciarsesion', name='login'),
    url(r'^inicio/$', 'Sigma_System.views.inicio', name='inicio'),
    url(r'^finalizar/$', 'Sigma_System.views.cerrarsesion', name='finalizar'),
    url(r'^adm_u/$', 'Sigma_System.views.adm_usuario', name='adm_u'),
    url(r'^adm_u_altas/$', 'Sigma_System.views.alta_usuario', name='adm_u_altas'),
    url(r'^nuevopass/$', 'Sigma_System.views.recuperarPass', name='recu_pass'),
    url(r'^cambiarPass/$', 'Sigma_System.views.cambiarPass', name='cambiarPass'),

    url(r'^adm_u_baja/(?P<us>\d+)$', 'Sigma_System.views.baja_usuario', name='adm_u_baja'),
    url(r'^adm_u_mod/(?P<us>\d+)/$', 'Sigma_System.views.modificar_usuario', name='adm_u_mod'),
    url(r'^adm_u_bus/$', 'Sigma_System.views.buscar_usuario', name='adm_u_bus'),
    url(r'^adm_u_ver/(?P<us>\d+)$', 'Sigma_System.views.ver_detalle', name='adm_u_ver'),
    url(r'^adm_u_cambiar/(?P<us>\d+)$', 'Sigma_System.views.cambiar', name='adm_u_cambiar'),

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
    url(r'^proyecto/(?P<idProyect>\d+)/fase/alta/$',
       'Sigma_System.vistas.FaseViews.alta_fase',
       name='adm_fase_alta'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/modificar/(?P<idFase>\d+)/$',
       'Sigma_System.vistas.FaseViews.modificar_fase',
       name='adm_fase_mod'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/baja/(?P<idFase>\d+)/$',
       'Sigma_System.vistas.FaseViews.baja_fase',
       name='adm_fase_baja'),

    url(r'^adm_i_alta/(?P<idFase>\d+)$', 'Sigma_System.vistas.ItemViews.altaItem', name='adm_i_alta'),
    url(r'^adm_i/(?P<idFase>\d+)$', 'Sigma_System.vistas.ItemViews.administrarItem', name='adm_i'),
    url(r'^adm_i_mod/(?P<it>\d+)/$', 'Sigma_System.vistas.ItemViews.modificar_item', name='adm_i_mod'),
    url(r'^adm_i_baja/(?P<it>\d+)/$', 'Sigma_System.vistas.ItemViews.baja_item', name='adm_i_baja'),
    url(r'^adm_i_rev/(?P<idFase>\d+)/$', 'Sigma_System.vistas.ItemViews.revivir_item', name='adm_i_rev'),
    url(r'^adm_i_revivir/(?P<it>\d+)/$', 'Sigma_System.vistas.ItemViews.revivir', name='adm_i_revivir'),
    url(r'^adm_i_revertir/(?P<idFase>\d+)/$', 'Sigma_System.vistas.ItemViews.revertir', name='adm_i_revertir'),
    url(r'^adm_i_revertirItem/(?P<idItem>\d+)/item/revertir/(?P<versionRev>\d+)/item/revertir/(?P<idHis>\d+)$', 'Sigma_System.vistas.ItemViews.revertirItem', name='adm_i_revertirItem'),
    url(r'^adm_i_historialItem/(?P<idItem>\d+)/$', 'Sigma_System.vistas.ItemViews.historialItem', name='adm_i_historialItem'),

    url(r'^item/relacion/(?P<id_item>\d+)/$', 'Sigma_System.vistas.RelacionItemViews.adm_relacion',
        name='adm_relacion'),
    url(r'^item/relacion/asignar_padre/(?P<id_item>\d+)/$', 'Sigma_System.vistas.RelacionItemViews.asignar_padre',
        name='adm_rel_asig_padre'),
    url(r'^item/relacion/asignar/final/(?P<hijo>\d+)/(?P<padre>\d+)/$',
        'Sigma_System.vistas.RelacionItemViews.asignar_final',
        name='adm_rel_asig_final'),
    url(r'^item/relacion/hijos/(?P<id_item>\d+)/$', 'Sigma_System.vistas.RelacionItemViews.ver_hijos',
        name='adm_rel_hijos'),

    url(r'^proyecto/(?P<idProyect>\d+)/fase/intercambiar/$',
       'Sigma_System.vistas.FaseViews.intercambiarFase',
       name='adm_fase_intercambiar'),
    ### Urls de Tipos de Item de una fase
    url(r'^proyecto/(?P<idProyect>\d+)/fase/(?P<idFase>\d+)'
        r'/tipoItem/$',
        'Sigma_System.vistas.TIViews.administrarTI',
        name='adm_ti'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/(?P<idFase>\d+)'
        r'/tipoItem/alta/$',
        'Sigma_System.vistas.TIViews.altaTI',
        name='adm_ti_alta'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/(?P<idFase>\d+)'
        r'/tipoItem/mod/(?P<idTI>\d+)/$',
        'Sigma_System.vistas.TIViews.modificarTI',
        name='adm_ti_mod'),
    url(r'^proyecto/(?P<idProyect>\d+)/fase/(?P<idFase>\d+)'
        r'/tipoItem/baja/(?P<idTI>\d+)/$',
        'Sigma_System.vistas.TIViews.bajaTI',
        name='adm_ti_baja'),
    url(r'^proyecto/fase/(?P<idFase>\d+)/tipoItem/importar/$',
        'Sigma_System.vistas.TIViews.importarTI',
        name='adm_ti_impor'),
    #Urls de atributos
    url(r'^proyecto/fase/tipoItem/(?P<idTI>\d+)'
        r'/atributo/$',
        'Sigma_System.vistas.AtributoViews.administrarAtributos',
        name='adm_atrib'),
    url(r'^proyecto/fase/tipoItem/(?P<idTI>\d+)'
        r'/atributo/alta/$',
        'Sigma_System.vistas.AtributoViews.altaAtributo',
        name='adm_atrib_alta'),
    url(r'^proyecto/fase/tipoItem/(?P<idTI>\d+)'
        r'/atributo/mod/(?P<idAtributo>\d+)/$',
        'Sigma_System.vistas.AtributoViews.modificarAtributo',
        name='adm_atrib_mod'),
    url(r'^proyecto/fase/tipoItem/(?P<idTI>\d+)'
        r'/atributo/baja/(?P<idAtributo>\d+)/$',
        'Sigma_System.vistas.AtributoViews.bajaAtributo',
        name='adm_atrib_baja'),
    url(r'^desarrollo/proyectos/$',
        'Sigma_System.vistas.ProyectoViews.administrarProyectosAsociados',
        name='des_proyec'),
    url(r'^proyecto/(?P<idProyect>\d+)/asignarUsuario/$',
        'Sigma_System.vistas.ProyectoViews.asignarUsuarioProyecto',
        name='adm_proy_asig_usu'),
    url(r'^proyecto/(?P<idProyect>\d+)/comite/$',
        'Sigma_System.vistas.ComiteViews.ComiteDeCambio',
        name='adm_proy_comite'),
    url(r'^proyecto/(?P<idProyect>\d+)/comite/$',
        'Sigma_System.vistas.ComiteViews.agregarUsuarios',
        name='adm_proy_comite_usuario'),
    url(r'^proyecto/(?P<idProyect>\d+)/iniciar/$',
        'Sigma_System.vistas.ProyectoViews.iniciarProyecto',
        name='adm_proy_iniciar'),
    url(r'^desarrollo/(?P<idFase>\d+)/intercambio/$',
        'Sigma_System.vistas.FaseViews.intercambiarFase',
        name='des_fase_intercambio'),
    )