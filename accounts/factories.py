import factory

from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Sequence(lambda n: 'johndoe%s@wishlist.com' % n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
