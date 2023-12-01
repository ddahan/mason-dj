from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.api_token import APIAccessToken

User = get_user_model()


class Command(BaseCommand):
    help = "For the specified user, revoque all existing api access tokens. This serves a safety purpose."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(f"User {email} not found in database.")

        with transaction.atomic():
            for token in APIAccessToken.objects.filter(user=user):
                token.revoque()

        self.stdout.write(f"All API Access tokens for {user} has been revoqued.")
