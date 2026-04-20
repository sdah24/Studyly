from django.test import TestCase
from django.urls import reverse

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipFilterTest(TestCase):

    def setUp(self):

        self.uni1 = University.objects.create(

            name="Harvard",
            country="USA"

        )

        self.uni2 = University.objects.create(

            name="Oxford",
            country="UK"

        )

        Scholarship.objects.create(

            title="Harvard Merit",

            description="Test",

            amount=5000,

            deadline="2030-01-01",

            university=self.uni1

        )

        Scholarship.objects.create(

            title="Oxford Grant",

            description="Test",

            amount=3000,

            deadline="2030-01-01",

            university=self.uni2

        )

    def test_filter_by_university(self):

        response = self.client.get(

            reverse("scholarships:search"),

            {

                "university":
                self.uni1.id

            }

        )

        self.assertContains(

            response,

            "Harvard Merit"

        )

    def test_filter_by_amount(self):

        response = self.client.get(

            reverse("scholarships:search"),

            {

                "min_amount": 4000

            }

        )

        self.assertContains(

            response,

            "Harvard Merit"

        )