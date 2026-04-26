from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):
    """TC-U01 through TC-U03, TC-U10"""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')