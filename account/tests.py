import json
from django.urls import reverse
from common.code import *
from .models import ExtendedUser as User
from rest_framework.test import APITestCase


class AccountCreateTests(APITestCase):
    def setUp(self):
        self.url = reverse('account-register')

    def tearDown(self):
        response = self.client.post(self.url, self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['code'], self.code)

    def test_correct_1(self):
        # correct password
        # correct email
        # correct name
        self.data = {
            'username': 'daddy',
            'password': '123ASDab123A',
            'email': 'abc@qq11.com',
            'first_name': 'test',
            'last_name': 'gg'
        }
        self.code = ACCOUNT_REGISTER_SUCCESS


class AccountLoginTests(APITestCase):

    def setUp(self):
        self.url = reverse('account-login')
        self.user = User.objects.create_user(username='daddy',
                                             password='passwordASD123',
                                             email='email@email.com',
                                             first_name='first',
                                             last_name='last')

    def tearDown(self):
        response = self.client.post(self.url, self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['code'], self.code)

    def test_correct_1(self):
        # correct credentials
        self.data = {
            'username': 'daddy',
            'password': 'passwordASD123'
        }
        self.code = ACCOUNT_LOGIN_SUCCESS


class AccountLogoutTests(APITestCase):

    def setUp(self):
        self.url = reverse('account-logout')
        self.user = User.objects.create_user(username='daddy',
                                             password='passwordASD123',
                                             email='email@email.com',
                                             first_name='first',
                                             last_name='last')
        data = {
            'username': 'daddy',
            'password': 'passwordASD123'
        }
        response = self.client.post(reverse('account-login'), data, format='json')
        content = json.loads(response.content)
        self.token = content['token']

    def tearDown(self):
        response = self.client.post(self.url, self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['code'], self.code)

    def test_correct_1(self):
        # correct token
        self.data = {
            'token': self.token
        }
        self.code = ACCOUNT_LOGOUT_SUCCESS


class AccountGetTests(APITestCase):

    def setUp(self):
        self.url = reverse('account-get')
        self.user = User.objects.create_user(username='daddy',
                                             password='passwordASD123',
                                             email='email@email.com',
                                             first_name='first',
                                             last_name='last')
        data = {
            'username': 'daddy',
            'password': 'passwordASD123'
        }
        response = self.client.post(reverse('account-login'), data, format='json')
        content = json.loads(response.content)
        self.token = content['token']

    def tearDown(self):
        response = self.client.post(self.url, self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['code'], self.code)
        if self.code == ACCOUNT_GET_SUCCESS:
            self.assertEqual(content['details']['first_name'], self.user.first_name)
            self.assertEqual(content['details']['last_name'], self.user.last_name)
            self.assertEqual(content['details']['email'], self.user.email)

    def test_correct_1(self):
        # correct token
        self.data = {
            'token': self.token
        }
        self.code = ACCOUNT_GET_SUCCESS

    def test_wrong_1(self):
        # wrong token
        self.data = {
            'token': 'abc'
        }
        self.code = ACCOUNT_TOKEN_ERROR
