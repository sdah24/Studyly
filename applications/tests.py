from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from universities.models import University
from applications.models import Application
import datetime

User = get_user_model()


def make_user(username='appuser', password='pass@123'):
    return User.objects.create_user(username=username, password=password, role='student')


def make_university():
    return University.objects.create(
        name='Test University', country='USA', city='Boston',
        ranking=10, min_gpa=3.0, min_ielts=6.5
    )


class ApplicationCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.university = make_university()
        self.list_url = reverse('applications:list')
        self.create_url = reverse('applications:create')

    def test_create_application_valid(self):
        self.client.login(username='appuser', password='pass@123')
        count_before = Application.objects.count()
        self.client.post(self.create_url, {
            'university': self.university.pk,
            'status': 'incomplete',
            'deadline': (datetime.date.today() + datetime.timedelta(days=30)).isoformat(),
            'personal_statement': 'My statement here.',
        })
        self.assertGreater(Application.objects.count(), count_before)

    def test_list_shows_only_own_applications(self):
        user_a = self.user
        user_b = make_user(username='userB')
        Application.objects.create(user=user_a, university=