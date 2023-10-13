from django.contrib.auth import get_user_model

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}@fakemail.com")
    title = "M"
    first_name = factory.Sequence(lambda n: f"User_{n + 1}")
    last_name = "fake"

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        """Override the default `_create` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)
