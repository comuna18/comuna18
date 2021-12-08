from django.core.management.base import BaseCommand, CommandError

from projects.models import Project
from django.apps import apps


class Command(BaseCommand):
    help = 'Add identifier to corresponding models'

    def handle(self, *args, **options):
        models = apps.get_models()
        for model in models:
            if 'identifier' in [field.name for field in model._meta.fields]:
                for item in model.objects.all():
                    item.identifier = item.get_identifier()
                    item.save()
