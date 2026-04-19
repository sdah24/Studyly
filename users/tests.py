
from django.test import TestCase
from .models import User
from django.urls import reverse

class UserModelTest(TestCase):

    def test_user_creation(self):

        user = User.objects.create(
            name="Test User",
            email="testuser@gmail.com",
            password="123456"
        )

        self.assertEqual(
            user.name,
            "Test User"
        )

        self.assertEqual(
            user.email,
            "testuser@gmail.com"
        )




class LoginTest(TestCase):

    def test_login_valid_user(self):

        User.objects.create(
            name="Login User",
            email="login@gmail.com",
            password="123456"
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "login@gmail.com",
                "password": "123456"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class ProfileTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.client.login(
            username="testuser",
            password="password123"
        )

    def test_profile_form_loads(self):

        response = self.client.get(
            reverse("users:create_profile")
        )

        self.assertEqual(response.status_code, 200)

    def test_profile_submission(self):

        response = self.client.post(

            reverse("users:create_profile"),

            {

                "full_name": "Test User",

                "phone_number": "123456789",

                "date_of_birth": "2000-01-01",

                "address": "Dhaka",

            }

        )

        self.assertEqual(response.status_code, 302)