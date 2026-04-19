from django.test import TestCase

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipModelTest(
    TestCase
):

    def setUp(self):

        self.university = University.objects.create(

            name="Test University",

            country="USA"

        )

    def test_create_scholarship(self):

        scholarship = Scholarship.objects.create(

            title="Test Scholarship",

            description="Testing",

            amount=5000,

            deadline="2030-01-01",

            university=self.university

        )

        self.assertEqual(

            scholarship.title,

            "Test Scholarship"

        )

        self.assertEqual(

            scholarship.university.name,

            "Test University"

        )