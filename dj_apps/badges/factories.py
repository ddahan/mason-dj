import random
from datetime import timedelta

from django.utils import timezone

import factory

from .models.badge import Badge


class BadgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Badge

    owner = factory.SubFactory("profiles.factories.UserFactory")

    @factory.lazy_attribute
    def expiration(self):
        return timezone.now() + timedelta(days=365)


class UnexpiredBadgeFactory(BadgeFactory):
    ...


class ExpiredBadgeFactory(BadgeFactory):
    @factory.lazy_attribute
    def expiration(self):
        return timezone.now() - timedelta(days=1)


class RandomBadgeFactory(BadgeFactory):
    @factory.lazy_attribute
    def expiration(self):
        random_minutes = random.randint(-100000, 100000)
        return timezone.now() + timedelta(minutes=random_minutes)

    @factory.lazy_attribute
    def is_active(self):
        return random.choice([True, False])
