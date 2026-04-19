from django.test import TestCase
from django.urls import reverse
from universities.models import University


class UniversityDisplayTest(TestCase):

    def setUp(self):
        self.uni = University.objects.create(
            name="Test University",
            country="USA"
        )

    def test_result_displayed(self):
        response = self.client.get(
            reverse("universities:search")
        )
        self.assertContains(
            response,
            "Test University"
        )

    def test_detail_page_loads(self):
        response = self.client.get(
            reverse(
                "universities:detail",
                args=[self.uni.id]
            )
        )
        self.assertEqual(
            response.status_code,
            200
        )