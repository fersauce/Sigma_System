from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client
from Sigma_System.views import iniciarsesion, inicio, adm_usuario
from django.core.urlresolvers import reverse
from Sigma_System.models import Usuario, Rol, Permiso, UsuarioRol
from django.utils.importlib import import_module
from django.conf import settings
from Sigma_System.funciones_aux import permisos_disponibles

class Testing(TestCase):
    """
    Clase para realizar los testings.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('admin', 'kandia88@gmail.com', 'admin')
        self.usuario = Usuario.objects.create(user=self.user, ci='4673',
                                              direccion='lejos',
                                              tel='021',
                                              estado=True)
        self.rol = Rol.objects.create(nombre="Administrador de Sistema",
                                      descripcion="Con este rol se establece el superusuario con todos los "
                                                  "permisos del sistema asignados")
        self.p1 = Permiso.objects.create(nombre="Super Usuario", codigo="super_us")
        self.p2 = Permiso.objects.create(nombre="Crear Usuario", codigo="crear_us")
        self.p3 = Permiso.objects.create(nombre="Modificar Usuario", codigo="modificar_us")
        self.p4 = Permiso.objects.create(nombre="Ver Usuario", codigo="ver_us")
        self.rol.permisos.add(self.p1)
        self.rol.permisos.add(self.p2)
        self.rol.permisos.add(self.p3)
        self.rol.permisos.add(self.p4)

        UsuarioRol.objects.create(usuario=self.user.usuario, rol=self.rol,
                                  idProyecto=0, idFase=0, idItem=0)
        self.c = Client()
        self.engine = import_module(settings.SESSION_ENGINE)
        self.permisos_disponibles = permisos_disponibles(self.user)

    def test_Usuario_login(self):
        request = self.factory.post(reverse('sigma:login'), {'username': 'admin', 'password': 'admin'})
        request.user = self.user
        request.session = self.engine.SessionStore()
        response = iniciarsesion(request)
        self.assertEqual(response.status_code, 302)

    def test_Usuario_inicio(self):
        request = self.factory.get(reverse('sigma:inicio'))
        request.user = self.user
        request.session = self.engine.SessionStore()
        request.session['permisos'] = self.permisos_disponibles
        response = inicio(request)
        self.assertEqual(response.status_code, 200)

    def testUsuario(self):
        """
        Test de la url de usuario.
        """
        request = self.factory.get(reverse('sigma:adm_u'))
        request.user = self.user
        request.session = self.engine.SessionStore()
        request.session['permisos'] = self.permisos_disponibles
        response = adm_usuario(request)
        self.assertEqual(response.status_code, 200)

    def testUsuarioComparacion(self):
        """
        Testing de comparacion de usuario test
        """
        user1 = User.objects.get(username='admin')
        self.assertEqual(self.user.email, user1.email)

    def tearDown(self):
        self.user.delete()