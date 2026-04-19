from django.test import TestCase
from django.urls import reverse

from universities.models import University


class UniversityPaginationTest(
    TestCase
):

    def setUp(self):

        for i in range(25):

            University.objects.create(
                name=f"University {i}",
                country="USA"
            )

    def test_pagination_page_1(self):

        response = self.client.get(

            reverse("universities:search")

        )

        self.assertEqual(

            response.status_code,

            200

        )

        self.assertContains(
            response,
            "Page 1"
        )

    def test_pagination_page_2(self):

        response = self.client.get(

            reverse("universities:search"),

            {"page": 2}

        )

        self.assertEqual(
            response.status_code,
            200
        )