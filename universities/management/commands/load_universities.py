from django.core.management.base import BaseCommand

from universities.models import University


class Command(BaseCommand):

    help = "Load sample universities"

    def handle(self, *args, **kwargs):

        universities = [

            {
                "name": "Harvard University",
                "country": "USA",
                "city": "Cambridge",
                "ranking": 1,
            },

            {
                "name": "MIT",
                "country": "USA",
                "city": "Cambridge",
                "ranking": 2,
            },

            {
                "name": "Oxford University",
                "country": "UK",
                "city": "Oxford",
                "ranking": 3,
            },

        ]

        for uni in universities:

            University.objects.get_or_create(
                name=uni["name"],
                defaults=uni
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Sample universities loaded."
            )
        )