from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework.test import APITestCase

from .factories import UserFactory
from .models import User
from .utils import uidb64_encode


class AccountsTestCase(TestCase):

    def test_cant_register_twice_with_same_email(self):
        """Email address must be unique"""
        UserFactory.create(email='foo@bar.com')

        with self.assertRaises(IntegrityError):
            UserFactory.create(email='FOO@BAR.COM')


class AccountsAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth_url = reverse('api:token-auth')
        cls.refresh_url = reverse('api:token-refresh')
        cls.verify_url = reverse('api:token-verify')
        cls.register_url = reverse('api:register')
        cls.activation_url = reverse('activate_user')

    def test_can_create_token(self):
        """An anonymous user can create an access token with valid credentials"""
        user = UserFactory.create(password='test')

        response = self.client.post(self.auth_url, {
            'email': user.email,
            'password': 'test'
        })

        self.assertEqual(response.status_code, 200)

    def test_cant_create_token_with_invalid_credentials(self):
        """An anonymous user can't create an access token with invalid credentials"""
        user = UserFactory.create(password='test')

        response = self.client.post(self.auth_url, {
            'email': user.email,
            'password': 'potato'
        })

        self.assertEqual(response.status_code, 400)

    def test_can_refresh_valid_token(self):
        """An anonymous user can refresh a valid token"""
        user = UserFactory.create(password='test')

        response = self.client.post(self.auth_url, {
            'email': user.email,
            'password': 'test'
        })

        token = response.data['token']

        response = self.client.post(self.refresh_url, {
            'token': token
        })

        self.assertEqual(response.status_code, 200)

    def test_cant_refresh_invalid_token(self):
        """An anonymous user can't refresh an invalid token"""
        response = self.client.post(self.refresh_url, {
            'token': 'potato'
        })

        self.assertEqual(response.status_code, 400)

    def test_verify_token(self):
        """An anonymous user can verify tokens"""
        user = UserFactory.create(password='test')

        response = self.client.post(self.auth_url, {
            'email': user.email,
            'password': 'test'
        })

        token = response.data['token']

        response = self.client.post(self.verify_url, {
            'token': token
        })

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.verify_url, {
            'token': 'potato'
        })

        self.assertEqual(response.status_code, 400)

    def test_can_register(self):
        """An anonymous user can register with valid data"""
        response = self.client.post(self.register_url, {
            'email': 'foo@bar.com',
            'password': 'potato'
        })

        self.assertEqual(response.status_code, 201)
        # self.assertIn('token', response.data)
        # self.assertEqual(response.data['email'], 'foo@bar.com')
        # self.assertNotIn('password', response.data)

    def test_cant_register_twice_the_same_email(self):
        """An anonymous user can't register twice with the same email"""
        user = UserFactory.create()

        response = self.client.post(self.register_url, {
            'email': user.email.upper(),
            'password': 'potato'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_user_activation(self):
        """
        given a not activated user
        when he GET the activation page with the url given by mail
        then he is activated
        """
        user = UserFactory.create(is_active=False)
        self.assertFalse(user.is_active)
        token = user.token_generator.make_token(user)
        response = self.client.get(self.activation_url, {
            'uid': uidb64_encode(user.pk),
            'token': token
        })
        user = User.objects.get(pk=user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)
