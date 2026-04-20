from django.test import TestCase
from django.urls import reverse

from universities.models import University
from scholarships.models import Scholarship


class DeleteScholarshipTest(TestCase):

    def setUp(self):

        self.university = University.objects.create(
            name="Delete University",
            country="USA"
        )

        self.scholarship = Scholarship.objects.create(
            title="Delete Me",
            description="Test",
            amount=1000,
            deadline="2030-01-01",
            university=self.university
        )

    def test_delete_scholarship(self):

        response = self.client.post(

            reverse(
                "scholarships:delete",
                args=[self.scholarship.id]
            )

        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(

            Scholarship.objects.filter(
                id=self.scholarship.id
            ).exists()

        )