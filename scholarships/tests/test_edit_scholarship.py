from django.test import TestCase
from django.urls import reverse

from universities.models import University
from scholarships.models import Scholarship


class EditScholarshipTest(
    TestCase
):

    def setUp(self):

        self.university = University.objects.create(

            name="Test University",
            country="USA"

        )

        self.scholarship = Scholarship.objects.create(

            title="Original Title",

            description="Test",

            amount=5000,

            deadline="2030-01-01",

            university=self.university

        )

    def test_edit_scholarship(self):

        response = self.client.post(

            reverse(

                "scholarships:edit",

                args=[self.scholarship.id]

            ),

            {

                "title":
                "Updated Title",

                "description":
                "Updated",

                "amount":
                "6000",

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

        self.scholarship.refresh_from_db()

        self.assertEqual(

            self.scholarship.title,

            "Updated Title"

        )