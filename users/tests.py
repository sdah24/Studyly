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


    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            username='loginuser', password='TestPass@123', role='student'
        )

    def test_login_with_correct_credentials(self):
        """TC-U04: Correct credentials → session created, redirect to dashboard."""
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'TestPass@123',
        })
        # Should redirect (302) after successful login
        self.assertEqual(response.status_code, 302)
        # User should now be logged in
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_with_wrong_password(self):
        """TC-U05: Wrong password → error shown, no session."""
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'WrongPass@999',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_clears_session(self):
        """TC-U06: Logout clears session."""
        self.client.login(username='loginuser', password='TestPass@123')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('users:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 302)


class UserProfileSignalTests(TestCase):
    """TC-U07"""

    def test_profile_auto_created_on_register(self):
        """TC-U07: Profile is auto-created when a User is saved."""
        from users.models import Profile
        user = User.objects.create_user(username='signaluser', password='pass@123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_is_one_to_one(self):
        """Only one Profile per User."""
        from users.models import Profile
        user = User.objects.create_user(username='uniqueprofile', password='pass@123')
        # Profile already created by signal; creating another should raise
        with self.assertRaises(Exception):
            Profile.objects.create(user=user)
