from django.test import TestCase
from django.urls import reverse

from universities.models import University


class AddScholarshipTest(
    TestCase
):

    def setUp(self):

        self.university = University.objects.create(

            name="Harvard",
            country="USA"

        )

    def test_add_scholarship(self):

        response = self.client.post(

            reverse("scholarships:add"),

            {

                "title":
                "Test Scholarship",

                "description":
                "Test Description",

                "amount":
                "5000",

                "deadline":
                "2030-01-01",

                "university":
                self.university.id,

            }

        )

        self.assertEqual(
            response.status_code,
            302
        )