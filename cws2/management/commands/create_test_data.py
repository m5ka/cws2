from django.core.management.base import BaseCommand

from cws2.fixtures import Fixtures


class Command(BaseCommand):
    help = (
        "Creates a suite of sample data to make testing the site during local "
        "development easier."
    )

    def handle(self, *args, **options):
        f = Fixtures(stdout=self.stdout)
        f.create_fixtures()
