from datetime import date

from django.test import TestCase

from accounts.factories import UserFactory

from .factories import InventoryFactory
from .models import Product


class ProductTestCase(TestCase):

    def setUp(self):
        self.inventory = InventoryFactory.create()
        self.user = UserFactory.create(email='too@earl.com')

    def test_calculation_of_notification_date(self):
        product = Product.objects.create(
            name='test',
            expiration_date='1994-05-01',
            notification_delay=1,
            inventory=self.inventory,
            user=self.user
        )
        self.assertEquals(product.notification_date, date.fromisoformat('1994-04-30'))
