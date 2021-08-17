from django.test import TestCase
from unipath import Path
from django.test import override_settings
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from freezegun import freeze_time
from datetime import datetime, timedelta
from .models import *
from django.contrib.auth.hashers import make_password
import ast

class RequirementsTestCase(TestCase):
    def setUp(self):
        self.value = 12

    def test_number_of_classes_greater_then_4(self):
        """Check if there is more than four classes implemented"""
        with open(Path(__file__).parent.child('models.py')) as f:
            tree = ast.parse(f.read())
            number_of_classes = sum(isinstance(exp, ast.ClassDef) for exp in tree.body)
        self.assertEqual(number_of_classes > 4, True)


class NonAuthenticatedAccessTestCase(APITestCase):
    def setUp(self):
        self.limit = 60
        self.url = reverse('api-stats')

    def test_non_user(self):
        for i in range(self.limit):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        freezer = freeze_time("2022-01-14 00:00:01")

        freezer.start()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        freezer.stop()


class AuthenticatedAccessTestCase(APITestCase):
    def setUp(self):
        self.limit = 600
        self.url = reverse('api-stats')
        self.restaurante_profile = RestaurantProfile.objects.create(username='Teste1', password=make_password('123'), phone='123')
        self.pessoa_profile = PersonProfile.objects.create(username='Teste2', password=make_password('123'), phone='1234')
        self.client = APIClient()

    def test_user(self):
        self.client.force_authenticate(user=self.pessoa_profile)

        for i in range(self.limit):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        freezer = freeze_time("2022-01-14 00:00:01")
        freezer.start()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        freezer.stop()

class RestauranteAccessTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('restaurant-list')
        self.client = APIClient()
        self.data = {'email': 'Sincere@april.biz', 'name': 'Sincere HEHE', 'phone': '4423', 'description': 'RED'}

    def test_can_access(self):
        self.restaurante_profile = User.objects.create(username='Teste1', password=make_password('1ewfewfefe23'),
                                                                    phone='123', email='teste@gmail.com', user_type = UserType.RESTAURANTE)
        self.client.force_authenticate(user=self.restaurante_profile)
        self.data['owner'] = self.restaurante_profile.pk

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_cannot_access(self):
        self.pessoa_profile = User.objects.create(username='Teste34', password=make_password('12efwefwfewefe3'),
                                                           phone='1234', email='teste2@gmail.com', user_type = UserType.CLIENTE)
        self.client.force_authenticate(user=self.pessoa_profile)

        self.data['owner'] = self.pessoa_profile.pk
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PessoaAccessTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('api-stats')
        self.restaurante_profile = RestaurantProfile.objects.create(username='Teste1', password=make_password('123'), phone='123')
        self.pessoa_profile = PersonProfile.objects.create(username='Teste2', password=make_password('123'), phone='1234')
        self.client = APIClient()
        self.data = {'username': 'Sincere@april.biz', 'password': 'Sincere@april.biz'}

    def test_can_access(self):
        pass
        #self.client.force_authenticate(user=self.pessoa_profile)
        #response = self.client.post(self.url, self.data)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_access(self):
        pass
        #self.client.force_authenticate(user=self.restaurante_profile)
        #response = self.client.post(self.url, self.data)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)