from django.core.management.base import BaseCommand
from universities.models import University, Program


UNIVERSITIES = [
    {
        "name": "Harvard University",
        "country": "USA", "city": "Cambridge",
        "ranking": 1, "rating": 4.9,
        "tuition_display": "$54,000/yr",
        "acceptance_rate": 4.5,
        "total_students": "31,000+",
        "established_year": 1636,
        "min_gpa": 3.5, "min_ielts": 7.0,
        "description": "Harvard University is a private Ivy League research university in Cambridge, Massachusetts. Established in 1636, it is the oldest institution of higher learning in the United States.",
        "website": "https://www.harvard.edu",
        "programs": [
            {"name": "Master of Computer Science", "level": "master", "duration": "2 years", "tuition_per_year": "$54,000"},
            {"name": "MBA", "level": "mba", "duration": "2 years", "tuition_per_year": "$73,440"},
            {"name": "Master of Public Health", "level": "master", "duration": "1-2 years", "tuition_per_year": "$65,000"},
            {"name": "Master of Education", "level": "master", "duration": "1 year", "tuition_per_year": "$52,000"},
            {"name": "Master of Architecture", "level": "master", "duration": "2.5 years", "tuition_per_year": "$54,000"},
        ]
    },
    {
        "name": "University of Oxford",
        "country": "UK", "city": "Oxford",
        "ranking": 2, "rating": 4.8,
        "tuition_display": "£28,000/yr",
        "acceptance_rate": 17.0,
        "total_students": "24,000+",
        "established_year": 1096,
        "min_gpa": 3.5, "min_ielts": 7.5,
        "description": "The University of Oxford is a collegiate research university in Oxford, England. There is evidence of teaching as far back as 1096, making it the oldest university in the English-speaking world.",
        "website": "https://www.ox.ac.uk",
        "programs": [
            {"name": "MSc in Computer Science", "level": "master", "duration": "1 year", "tuition_per_year": "£28,000"},
            {"name": "MSc in Data Science", "level": "master", "duration": "1 year", "tuition_per_year": "£30,000"},
            {"name": "MBA", "level": "mba", "duration": "1 year", "tuition_per_year": "£52,000"},
            {"name": "DPhil in Engineering", "level": "phd", "duration": "3-4 years", "tuition_per_year": "£26,000"},
        ]
    },
    {
        "name": "MIT",
        "country": "USA", "city": "Cambridge",
        "ranking": 3, "rating": 4.9,
        "tuition_display": "$55,000/yr",
        "acceptance_rate": 6.7,
        "total_students": "11,000+",
        "established_year": 1861,
        "min_gpa": 3.7, "min_ielts": 7.0,
        "description": "The Massachusetts Institute of Technology is a private land-grant research university in Cambridge, Massachusetts. MIT has played a key role in the development of modern technology and science.",
        "website": "https://www.mit.edu",
        "programs": [
            {"name": "Master of Artificial Intelligence", "level": "master", "duration": "2 years", "tuition_per_year": "$55,000"},
            {"name": "Master of Engineering", "level": "master", "duration": "1 year", "tuition_per_year": "$55,000"},
            {"name": "PhD in Computer Science", "level": "phd", "duration": "4-6 years", "tuition_per_year": "$55,000"},
        ]
    },
    {
        "name": "Stanford University",
        "country": "USA", "city": "Stanford",
        "ranking": 4, "rating": 4.8,
        "tuition_display": "$56,000/yr",
        "acceptance_rate": 5.2,
        "total_students": "17,000+",
        "established_year": 1885,
        "min_gpa": 3.6, "min_ielts": 7.0,
        "description": "Stanford University is a private research university in Stanford, California. It is one of the world's leading research and teaching institutions, situated in the heart of Silicon Valley.",
        "website": "https://www.stanford.edu",
        "programs": [
            {"name": "MBA", "level": "mba", "duration": "2 years", "tuition_per_year": "$56,000"},
            {"name": "MS in Computer Science", "level": "master", "duration": "1-2 years", "tuition_per_year": "$56,000"},
            {"name": "MS in AI", "level": "master", "duration": "1-2 years", "tuition_per_year": "$56,000"},
        ]
    },
    {
        "name": "University of Cambridge",
        "country": "UK", "city": "Cambridge",
        "ranking": 5, "rating": 4.8,
        "tuition_display": "£27,000/yr",
        "acceptance_rate": 21.0,
        "total_students": "23,000+",
        "established_year": 1209,
        "min_gpa": 3.5, "min_ielts": 7.5,
        "description": "The University of Cambridge is a collegiate research university in Cambridge, United Kingdom. Founded in 1209, it is the world's third-oldest university in continuous operation.",
        "website": "https://www.cam.ac.uk",
        "programs": [
            {"name": "MPhil in Advanced Computer Science", "level": "master", "duration": "1 year", "tuition_per_year": "£27,000"},
            {"name": "PhD in Engineering", "level": "phd", "duration": "3-4 years", "tuition_per_year": "£25,000"},
            {"name": "MBA", "level": "mba", "duration": "1 year", "tuition_per_year": "£54,000"},
        ]
    },
    {
        "name": "ETH Zurich",
        "country": "Switzerland", "city": "Zurich",
        "ranking": 8, "rating": 4.7,
        "tuition_display": "CHF 1,500/yr",
        "acceptance_rate": 27.0,
        "total_students": "22,000+",
        "established_year": 1855,
        "min_gpa": 3.3, "min_ielts": 7.0,
        "description": "ETH Zurich is a public research university in Zürich, Switzerland. It was founded in 1855 and is consistently ranked among the top universities in the world for science and technology.",
        "website": "https://ethz.ch",
        "programs": [
            {"name": "MSc in Computer Science", "level": "master", "duration": "2 years", "tuition_per_year": "CHF 1,500"},
            {"name": "MSc in Data Science", "level": "master", "duration": "2 years", "tuition_per_year": "CHF 1,500"},
            {"name": "PhD in Engineering", "level": "phd", "duration": "3-5 years", "tuition_per_year": "CHF 1,500"},
        ]
    },
]


class Command(BaseCommand):
    help = 'Load sample university data into the database'

    def handle(self, *args, **kwargs):
        for data in UNIVERSITIES:
            programs_data = data.pop('programs', [])

            uni, created = University.objects.update_or_create(
                name=data['name'],
                defaults=data
            )

            # Add programs
            for p in programs_data:
                Program.objects.update_or_create(
                    university=uni,
                    name=p['name'],
                    defaults=p
                )

            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status}: {uni.name}'))

        self.stdout.write(self.style.SUCCESS('Done loading universities!'))