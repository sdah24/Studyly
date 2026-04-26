from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):


    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')

    def test_register_with_valid_data(self):

        response = self.client.post(self.register_url, {
        'username': 'testuser',
        'email': 'test@example.com',
         'password1': 'StrongPass@123',
                'password2': 'StrongPass@123',
         })
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
        self.assertRedirects(response, reverse('users:login'))