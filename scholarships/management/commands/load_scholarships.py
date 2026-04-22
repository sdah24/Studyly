from django.core.management.base import BaseCommand

from universities.models import University
from scholarships.models import Scholarship


class Command(BaseCommand):

    help = "Load sample scholarships"

    def handle(self, *args, **kwargs):

        university = University.objects.first()

        if not university:

            self.stdout.write(

                self.style.WARNING(

                    "No universities found."

                )

            )

            return

        scholarships = [

            {

                "title": "Merit Scholarship",

                "description":
                "Academic excellence award.",

                "amount": 5000,

                "deadline": "2030-01-01",

            },

            {

                "title": "International Scholarship",

                "description":
                "For international students.",

                "amount": 8000,

                "deadline": "2030-06-01",

            },

        ]

        for item in scholarships:

            Scholarship.objects.get_or_create(

                title=item["title"],

                defaults={

                    **item,

                    "university": university

                }

            )

        self.stdout.write(

            self.style.SUCCESS(

                "Scholarships loaded."

            )

        )