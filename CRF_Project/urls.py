from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^ss/', include('Sigma_System.urls', namespace="sigma")),
    url(r'^login/', 'Sigma_System.views.iniciarsesion', name="log_in"),
    url(r'^admin/', include(admin.site.urls)),
)

