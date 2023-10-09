from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.api_token import APIToken

User = get_user_model()


class Command(BaseCommand):
    help = "For the specified user, delete the old API token and create a new one."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(f"User {email} not found in database.")

        new_token = APIToken.objects.create()
        self.stdout.write(
            f"Token {new_token.key} for {user} has been created. Older has been deleted."
        )
