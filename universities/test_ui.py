from django.test import TestCase
from django.urls import reverse


class UniversitySearchUITest(TestCase):

    def test_search_page_loads(self):

        response = self.client.get(

            reverse("universities:search")

        )

        self.assertEqual(

            response.status_code,

            200

        )