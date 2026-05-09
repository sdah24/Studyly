from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from universities.models import University
from scholarships.models import Scholarship

User = get_user_model()


class AdminPanelAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='adminuser', password='admin@123', role='admin'
        )
        self.student_user = User.objects.create_user(
            username='studentuser', password='student@123', role='student'
        )
        self.admin_url = reverse('adminpanel:dashboard')

    def test_admin_dashboard_loads_for_admin(self):
        self.client.login(username='adminuser', password='admin@123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_blocked(self):
        self.client.login(username='studentuser', password='student@123')
        response = self.client.get(self.admin_url)
        self.assertIn(response.status_code, [302, 403])

    def test_unauthenticated_blocked(self):
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)

    def test_students_list_visible_to_admin(self):
        self.client.login(username='adminuser', password='admin@123')
        url = reverse('adminpanel:students')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_university(self):
        self.client.login(username='adminuser', password='admin@123')
        count_before = University.objects.count()
        url = reverse('adminpanel:universities')
        self.client.post(url, {
            'name': 'New Test University',
            'country': 'Canada',
            'city': 'Toronto',
            'ranking': 50,
            'min_gpa': 3.0,
            'min_ielts': 6.5,
        })
        self.assertGreater(University.objects.count(), count_before)

    def test_admin_can_delete_scholarship(self):
        scholarship = Scholarship.objects.create(
            title='Delete Me', provider='Test', amount=5000,
            min_gpa_required=3.0, min_ielts_required=6.0
        )
        self.client.login(username='adminuser', password='admin@123')
        count_before = Scholarship.objects.count()
        url = reverse('adminpanel:scholarships')
        self.client.post(url, {'action': 'delete', 'pk': scholarship.pk})
        self.assertLessEqual(Scholarship.objects.count(), count_before)
