from django.test import TestCase
from django.urls import reverse

from universities.models import University


class UniversitySearchBackendTest(
    TestCase
):

    def setUp(self):

        University.objects.create(
            name="Harvard University"
        )

        University.objects.create(
            name="Oxford University"
        )

    def test_search_returns_results(self):

        response = self.client.get(

            reverse("universities:search"),

            {

                "query":
                "Harvard"

            }

        )

        self.assertContains(
            response,
            "Harvard University"
        )

    def test_search_no_results(self):

        response = self.client.get(

            reverse("universities:search"),

            {

                "query":
                "XYZ"

            }

        )

        self.assertContains(
            response,
            "No universities found."
        )