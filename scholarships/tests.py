from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from scholarships.models import Scholarship

User = get_user_model()


class ScholarshipListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='scholuser', password='pass@123')
        self.list_url = reverse('scholarships:list')
        self.fulbright = Scholarship.objects.create(
            title='Fulbright Scholarship', provider='US Government',
            amount=50000, funding_type='full', min_gpa_required=3.5, min_ielts_required=7.0
        )
        self.daad = Scholarship.objects.create(
            title='DAAD Scholarship', provider='Germany',
            amount=20000, funding_type='partial', min_gpa_required=3.0, min_ielts_required=6.5
        )

    def test_list_renders(self):
        self.client.login(username='scholuser', password='pass@123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_search_by_title(self):
        self.client.login(username='scholuser', password='pass@123')
        response = self.client.get(self.list_url, {'search': 'Fulbright'})
        self.assertContains(response, 'Fulbright')
        self.assertNotContains(response, 'DAAD')

    def test_funding_type_filter(self):
        self.client.login(username='scholuser', password='pass@123')
        response = self.client.get(self.list_url, {'funding': 'full'})
        self.assertContains(response, 'Fulbright')
        self.assertNotContains(response, 'DAAD')

    def test_unauthenticated_redirects(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)


class ScholarshipDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='detailscholuser', password='pass@123')
        from datetime import date
        self.scholarship = Scholarship.objects.create(
            title='Chevening', provider='UK Government',
            amount=40000, funding_type='full',
            deadline=date(2025, 12, 31),
            min_gpa_required=3.3, min_ielts_required=6.5
        )

    def test_detail_loads(self):
        self.client.login(username='detailscholuser', password='pass@123')
        url = reverse('scholarships:detail', args=[self.scholarship.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chevening')

    def test_detail_shows_deadline(self):
        self.client.login(username='detailscholuser', password='pass@123')
        url = reverse('scholarships:detail', args=[self.scholarship.pk])
        response = self.client.get(url)
        self.assertContains(response, '2025')

    def test_nonexistent_scholarship_404(self):
        self.client.login(username='detailscholuser', password='pass@123')
        url = reverse('scholarships:detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ScholarshipSeedTests(TestCase):
    def test_seed_loads_6_scholarships(self):
        from django.core.management import call_command
        call_command('load_scholarships', verbosity=0)
        self.assertEqual(Scholarship.objects.count(), 6)