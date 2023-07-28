from django.core.management.base import BaseCommand
from ...utils import delete_all_data

class Command(BaseCommand):
    help = 'Remove all data from the database'

    def handle(self, *args, **options):
        delete_all_data()

        self.stdout.write(self.style.SUCCESS('All data removed from database'))
