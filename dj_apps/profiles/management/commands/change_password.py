from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Change password of a given user, identified by its email address."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("--password", type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(f"User {email} not found in database.")
        else:
            password = options["password"]
            user.set_password(password)
            user.save()  # Reminder: set_password does not save the User object

            self.stdout.write(f"{user} password is now: {password}.")
