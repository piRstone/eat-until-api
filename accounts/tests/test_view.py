from datetime import date
from unittest import mock

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from ..models import User
from ..factories import UserFactory

from accounts.utils import uidb64_encode


class TestUserMeAPIView(APITestCase):
    fixtures = ['initial_data.dev.json']

    def test_me_anonymous(self):
        response = self.client.get(reverse('api:users-me'))
        self.assertEqual(response.status_code, 403)

    def test_me(self):
        User = get_user_model()
        self.client.force_authenticate(User.objects.first())
        response = self.client.get(reverse('api:users-me'))
        self.assertEqual(response.status_code, 200)


class TestUserActivateAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_active=False)
        cls.valid_token = User.token_generator.make_token(cls.user)
        cls.url = reverse('api:users-activate')

    def test_invalid_uidb64(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode('test'),
            'token': self.valid_token,
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('uidb64', response.data)
        self.assertIn('An error occured', response.data['uidb64'])

    def test_unknown_user(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(99999),
            'token': self.valid_token,
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('uidb64', response.data)
        self.assertIn('An error occured', response.data['uidb64'])

    def test_invalid_token(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': 'tooooken',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('token', response.data)
        self.assertIn('This link has expired. Please ask for a new one.', response.data['token'])

    def test_token_expired(self):
        from django.contrib.auth.tokens import PasswordResetTokenGenerator as TokenGenerator

        with mock.patch.object(TokenGenerator, '_today') as mock_token_generator:
            mock_token_generator.return_value = date(2018, 7, 15)  # Weeeee are the Champioooooon
            token_past = User.token_generator.make_token(self.user)

        assert token_past != self.valid_token, 'Go to "Euros millions" AZAP!!'

        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': token_past,
        })
        self.assertIn('token', response.data)
        self.assertIn('This link has expired. Please ask for a new one.', response.data['token'])

    def test_activate_success(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': self.valid_token,
        })
        self.assertEqual(response.status_code, 200)


class TestUserForgotPasswordAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse('api:users-forgot-password')

    def test_unknown_email(self):
        response = self.client.post(self.url, data={
            'email': 'foo@bar.com',
        })
        self.assertEqual(response.status_code, 200)

    def test_known_email(self):
        response = self.client.post(self.url, data={
            'email': self.user.email,
        })
        self.assertEqual(response.status_code, 200)


class TestUserResetPasswordAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.valid_token = User.token_generator.make_token(cls.user)
        cls.url = reverse('api:users-reset-password')

    def test_invalid_uidb64(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode('test'),
            'token': self.valid_token,
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('uidb64', response.data)
        self.assertIn('An error occured', response.data['uidb64'])

    def test_unknown_user(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(99999),
            'token': self.valid_token,
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('uidb64', response.data)
        self.assertIn('An error occured', response.data['uidb64'])

    def test_invalid_token(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': 'tooooken',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('token', response.data)
        self.assertIn('This link has expired. Please ask for a new one.', response.data['token'])

    def test_token_expired(self):
        from django.contrib.auth.tokens import PasswordResetTokenGenerator as TokenGenerator

        with mock.patch.object(TokenGenerator, '_today') as mock_token_generator:
            mock_token_generator.return_value = date(2018, 7, 15)  # Weeeee are the Champioooooon
            token_past = User.token_generator.make_token(self.user)

        assert token_past != self.valid_token, 'Go to "Euros millions" AZAP!!'

        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': token_past,
            'password1': 'password',
            'password2': 'password',
        })
        self.assertIn('token', response.data)
        self.assertIn('This link has expired. Please ask for a new one.', response.data['token'])

    def test_non_matching_passwords(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': self.valid_token,
            'password1': 'password',
            'password2': 'foo',
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Password don\'t match.', response.data['non_field_errors'])

    def test_reset_password_success(self):
        response = self.client.post(self.url, data={
            'uidb64': uidb64_encode(self.user.pk),
            'token': self.valid_token,
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 200)
