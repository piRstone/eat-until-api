import factory

from django.conf import settings
from django.utils.translation import get_language, to_locale

language = get_language() or 'fr-fr'
locale = to_locale(language)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    first_name = factory.Faker('first_name', locale=locale)
    last_name = factory.Faker('last_name', locale=locale)
    email = factory.Sequence(lambda n: 'johndoe%s@eatuntil.com' % n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
