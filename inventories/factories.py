import factory

from accounts.factories import UserFactory

from .models import Inventory


class InventoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Inventory

    name = "My list"
    user = factory.Subfactory(UserFactory)
