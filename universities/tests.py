from django.test import TestCase
from .models import University


class UniversityTest(TestCase):

    def test_university_creation(self):

        uni = University.objects.create(
            name="MIT",
            country="USA",
            tuition_range="$50000",
            intake="Fall",
            description="Top engineering university"
        )

        self.assertEqual(
            uni.name,
            "MIT"
        )