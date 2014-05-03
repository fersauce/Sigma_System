from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


def permisos_requeridos(permisos_var, redirec, mensaje):
    def decorador(vista):
        def _wraped_view(request, *args, **kwargs):
            c = 0
            for p in permisos_var:
                if p in request.session['permisos']:
                    c = c + 1
            if c == permisos_var.__len__():
                return vista(request, *args, **kwargs)
            else:
                messages.error(request, "No posee los permisos para "+mensaje)
                return HttpResponseRedirect(reverse(redirec))
        return _wraped_view
    return decorador