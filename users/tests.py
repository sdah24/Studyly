
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