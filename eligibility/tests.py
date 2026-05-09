from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile
from universities.models import University
from scholarships.models import Scholarship

User = get_user_model()


class EligibilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.check_url = reverse('eligibility:check')

        self.user_high = User.objects.create_user(username='highuser', password='pass@123', role='student')
        profile_high = Profile.objects.get(user=self.user_high)
        profile_high.gpa = 3.9
        profile_high.english_score = 8.0
        profile_high.english_proficiency = 'ielts'
        profile_high.degree_level = 'bachelors'
        profile_high.save()

        self.user_low = User.objects.create_user(username='lowuser', password='pass@123', role='student')
        profile_low = Profile.objects.get(user=self.user_low)
        profile_low.gpa = 2.3
        profile_low.english_score = 5.0
        profile_low.english_proficiency = 'ielts'
        profile_low.degree_level = 'bachelors'
        profile_low.save()

        University.objects.create(name='Harvard', country='USA', city='Cambridge',
                                   ranking=1, min_gpa=3.7, min_ielts=7.0)
        University.objects.create(name='Simple College', country='USA', city='NYC',
                                   ranking=100, min_gpa=2.0, min_ielts=4.5)

        Scholarship.objects.create(title='Merit Award', provider='Test',
                                    amount=10000, min_gpa_required=3.5, min_ielts_required=7.0)

    def test_eligibility_check_renders(self):
        self.client.login(username='highuser', password='pass@123')
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 200)

    def test_high_gpa_matches_universities(self):
        self.client.login(username='highuser', password='pass@123')
        response = self.client.get(self.check_url)
        matched = response.context.get('matched_universities', [])
        names = [u.name for u in matched]
        self.assertIn('Harvard', names)

    def test_low_gpa_matches_fewer_universities(self):
        self.client.login(username='highuser', password='pass@123')
        response_high = self.client.get(self.check_url)
        self.client.logout()
        self.client.login(username='lowuser', password='pass@123')
        response_low = self.client.get(self.check_url)
        high_count = len(response_high.context.get('matched_universities', []))
        low_count = len(response_low.context.get('matched_universities', []))
        self.assertLessEqual(low_count, high_count)

    def test_score_between_0_and_100(self):
        self.client.login(username='highuser', password='pass@123')
        response = self.client.get(self.check_url)
        score = response.context.get('score', -1)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_scholarship_match_uses_min_gpa(self):
        self.client.login(username='highuser', password='pass@123')
        response = self.client.get(self.check_url)
        matched_scholarships = response.context.get('matched_scholarships', [])
        titles = [s.title for s in matched_scholarships]
        self.assertIn('Merit Award', titles)

    def test_eligibility_requires_login(self):
        response = self.client.get(self.check_url)
        self.assertEqual(response.status_code, 302)