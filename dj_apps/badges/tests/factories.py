from datetime import timedelta

from django.utils import timezone

import factory

from ..models.badge import Badge


class BadgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Badge

    owner = factory.SubFactory("profiles.tests.factories.UserFactory")

    @factory.lazy_attribute
    def expiration(self):
        return timezone.now() + timedelta(days=365)


class UnexpiredBadgeFactory(BadgeFactory):
    ...


class ExpiredBadgeFactory(BadgeFactory):
    @factory.lazy_attribute
    def expiration(self):
        return timezone.now() - timedelta(days=1)
