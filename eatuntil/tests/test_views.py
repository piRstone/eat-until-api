from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse

from rest_framework.test import APITestCase

from accounts.factories import UserFactory


class ResetPasswordTestCase(TestCase):

    def setUp(self):
        UserFactory.create(email='foo@bar.com')

    def test_access_reset_password_page(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_post_reset_password_data(self):
        response = self.client.post(reverse('password_reset'),
                                    {'email': 'foo@bar.com'})
        self.assertEqual(response.status_code, 302)

    def test_get_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_get_password_reset_done(self):
        response = self.client.get(reverse('password_reset_confirm', args=('foo', 'bar')))
        self.assertEqual(response.status_code, 200)

    def test_get_password_reset_done(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
