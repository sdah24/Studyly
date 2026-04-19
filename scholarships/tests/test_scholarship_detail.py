from django.test import TestCase
from django.urls import reverse

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipDetailTest(TestCase):

    def setUp(self):

        university = University.objects.create(

            name="Stanford",

            country="USA"

        )

        self.scholarship = Scholarship.objects.create(

            title="Stanford Merit",

            description="Test",

            amount=7000,

            deadline="2030-01-01",

            university=university

        )

    def test_detail_page_loads(self):

        response = self.client.get(

            reverse(

                "scholarships:detail",

                args=[self.scholarship.id]

            )

        )

        self.assertEqual(

            response.status_code,

            200

        )

    def test_detail_content_displayed(self):

        response = self.client.get(

            reverse(

                "scholarships:detail",

                args=[self.scholarship.id]

            )

        )

        self.assertContains(

            response,

            "Stanford Merit"

        )