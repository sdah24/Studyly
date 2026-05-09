from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from universities.models import University, Program

User = get_user_model()


class UniversityListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='uniuser', password='pass@123')
        self.list_url = reverse('universities:list')
        self.harvard = University.objects.create(
            name='Harvard University', country='USA', city='Cambridge',
            ranking=1, min_gpa=3.7, min_ielts=7.0
        )
        self.oxford = University.objects.create(
            name='Oxford University', country='UK', city='Oxford',
            ranking=2, min_gpa=3.5, min_ielts=7.5
        )

    def test_university_list_renders(self):
        self.client.login(username='uniuser', password='pass@123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_search_by_name_filters_results(self):
        self.client.login(username='uniuser', password='pass@123')
        response = self.client.get(self.list_url, {'search': 'Harvard'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harvard')
        self.assertNotContains(response, 'Oxford')

    def test_country_filter_works(self):
        self.client.login(username='uniuser', password='pass@123')
        response = self.client.get(self.list_url, {'country': 'UK'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oxford')
        self.assertNotContains(response, 'Harvard')

    def test_unauthenticated_redirects_to_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.url)


class UniversityDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='detailuser', password='pass@123')
        self.university = University.objects.create(
            name='MIT', country='USA', city='Cambridge',
            ranking=3, min_gpa=3.8, min_ielts=7.0
        )
        self.program = Program.objects.create(
            university=self.university,
            name='Computer Science',
            level='Masters',
            duration='2 years',
            tuition_per_year=55000
        )

    def test_university_detail_loads(self):
        self.client.login(username='detailuser', password='pass@123')
        url = reverse('universities:detail', args=[self.university.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MIT')

    def test_detail_shows_programs(self):
        self.client.login(username='detailuser', password='pass@123')
        url = reverse('universities:detail', args=[self.university.pk])
        response = self.client.get(url)
        self.assertContains(response, 'Computer Science')

    def test_nonexistent_university_returns_404(self):
        self.client.login(username='detailuser', password='pass@123')
        url = reverse('universities:detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class UniversitySeedTests(TestCase):
    def test_seed_command_loads_6_universities(self):
        from django.core.management import call_command
        call_command('load_universities', verbosity=0)
        self.assertEqual(University.objects.count(), 6)