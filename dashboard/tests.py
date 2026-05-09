from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from universities.models import University
from applications.models import Application
import datetime

User = get_user_model()


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='dashuser', password='pass@123', role='student')
        self.dashboard_url = reverse('dashboard:dashboard')
        self.university = University.objects.create(
            name='Dash University', country='USA', city='Boston',
            ranking=5, min_gpa=3.0, min_ielts=6.5
        )

    def test_dashboard_loads_authenticated(self):
        self.client.login(username='dashuser', password='pass@123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.url)

    def test_application_count_in_context(self):
        Application.objects.create(user=self.user, university=self.university, status='submitted',
                                    deadline=datetime.date.today() + datetime.timedelta(days=10))
        Application.objects.create(user=self.user, university=self.university, status='incomplete',
                                    deadline=datetime.date.today() + datetime.timedelta(days=20))
        self.client.login(username='dashuser', password='pass@123')
        response = self.client.get(self.dashboard_url)
        self.assertIn('total_applications', response.context)
        self.assertEqual(response.context['total_applications'], 2)

    def test_accepted_count_in_context(self):
        Application.objects.create(user=self.user, university=self.university, status='accepted',
                                    deadline=datetime.date.today() + datetime.timedelta(days=10))
        self.client.login(username='dashuser', password='pass@123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context.get('accepted_applications'), 1)

    def test_profile_redirect(self):
        self.client.login(username='dashuser', password='pass@123')
        url = reverse('dashboard:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)