from django.test import TestCase

from universities.models import University


class UniversityModelTest(
    TestCase
):

    def test_university_creation(self):

        university = University.objects.create(

            name="Test University",

            country="USA",

            city="New York",

            ranking=10

        )

        self.assertEqual(

            university.name,

            "Test University"

        )

        self.assertEqual(

            university.country,

            "USA"

        )