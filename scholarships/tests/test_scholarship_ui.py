from django.test import TestCase
from django.urls import reverse


class ScholarshipSearchUITest(TestCase):

    def test_page_loads(self):

        response = self.client.get(

            reverse("scholarships:search")

        )

        self.assertEqual(

            response.status_code,

            200

        )
