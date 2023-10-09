from django.core.management.base import BaseCommand

from core.utils.shell_utils import sh


class Command(BaseCommand):
    help = "Find and erase all migrations files in the whole Django project."

    def handle(self, *args, **options):
        sh("find . -path */migrations/*.py -not -name __init__.py -delete")
        sh("find . -path */migrations/*.pyc -delete")
        self.stdout.write("All migration files have been deleted.")
