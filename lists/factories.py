import factory

from accounts.factories import UserFactory

from .models import List


class ListFactory(factory.DjangoModelFactory):

    class Meta:
        model = List

    name = "My list"
    user = factory.Subfactory(UserFactory)
