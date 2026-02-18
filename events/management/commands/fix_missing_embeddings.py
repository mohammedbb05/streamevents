from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient


class Command(BaseCommand):
    help = "Ensure all Event documents have an 'embedding' field (set to None)"

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        # Djongo uses collection names like '<app>_<model>' by default
        coll = db['events_event']
        result = coll.update_many({'embedding': {'$exists': False}}, {'$set': {'embedding': None}})
        self.stdout.write(self.style.SUCCESS(
            f"Matched {result.matched_count}, modified {result.modified_count} documents."))
