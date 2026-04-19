from django.test import TestCase
from django.urls import reverse

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipSearchTest(TestCase):

    def setUp(self):

        university = University.objects.create(

            name="Harvard",

            country="USA"

        )

        Scholarship.objects.create(

            title="Merit Scholarship",

            description="Test",

            amount=5000,

            deadline="2030-01-01",

            university=university

        )

    def test_search_returns_result(self):

        response = self.client.get(

            reverse("scholarships:search"),

            {

                "query":
                "Merit"

            }

        )

        self.assertContains(

            response,

            "Merit Scholarship"

        )

    def test_search_no_results(self):

        response = self.client.get(

            reverse("scholarships:search"),

            {

                "query":
                "XYZ"

            }

        )

        self.assertContains(

            response,

            "No scholarships found."

        )