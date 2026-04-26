from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):


    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')