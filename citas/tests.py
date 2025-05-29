from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class LoginTestCase(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_correcto(self):
        url = "/api/login/"
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("mensaje", response.data)
        self.assertEqual(response.data["mensaje"], "Login exitoso")

    def test_login_incorrecto(self):
        url = "/api/login/"
        data = {
            "username": self.username,
            "password": "contramal"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

