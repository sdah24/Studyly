from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):
    """TC-U01 through TC-U03, TC-U10"""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')

    def test_register_with_valid_data(self):
        """TC-U01: Valid registration creates user and redirects to login."""
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
        self.assertRedirects(response, reverse('users:login'))

    def test_register_with_duplicate_username(self):
        """TC-U02: Duplicate username shows form error, no new user created."""
        User.objects.create_user(username='existing', password='pass@123')
        count_before = User.objects.count()
        response = self.client.post(self.register_url, {
            'username': 'existing',
            'email': 'new@example.com',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), count_before)

    def test_register_with_mismatched_passwords(self):
        """TC-U03: Mismatched passwords → form error, user not created."""
        count_before = User.objects.count()
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass@123',
            'password2': 'DifferentPass@456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), count_before)

    def test_register_sets_role_student(self):
        """TC-U10: Registration sets role=student by default."""
        self.client.post(self.register_url, {
            'username': 'studentuser',
            'email': 'student@example.com',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })
        user = User.objects.get(username='studentuser')
        self.assertEqual(user.role, 'student')

    def test_register_page_loads(self):
        """GET registration page returns 200."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)


class UserLoginTests(TestCase):
    """TC-U04 through TC-U06"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            username='loginuser', password='TestPass@123', role='student'
        )
