from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
import Sigma_System
from Sigma_System import vistas, views


class Testing(TestCase):
    """
    Clase para realizar los testings.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('test', 'fersa1990@gmail.com', 'test')



    def testUsuario(self):
        """
        Test de la url de usuario.
        """
        request = self.factory.get("/ss/adm_u/")
        request.user = self.user
        response = views.adm_usuario(request)
        print self.assertEqual(response.status_code, 200)


    '''def testUsuarioComparacion(self):
        """
        Testing de comparacion de usuario test
        """
        user1 = User.objects.get(username='test')
        self.assertEqual(self.user.email, user1.email)


    def testLogin(self):
        """
        Testeo de Login
        """
        self.assertTrue(self.client.login(username='test', password='test'))'''



    def tearDown(self):
        self.user.delete()

