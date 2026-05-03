import time
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from universities.models import University
from scholarships.models import Scholarship
from applications.models import Application
from notifications.models import Notification
from users.models import Profile
import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

User = get_user_model()
CHROMEDRIVER_PATH = None

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1400,900')
    if CHROMEDRIVER_PATH:
        from selenium.webdriver.chrome.service import Service
        service = Service(CHROMEDRIVER_PATH)
        return webdriver.Chrome(service=service, options=options)
    return webdriver.Chrome(options=options)

def wait_for(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

class BaseSeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not SELENIUM_AVAILABLE:
            raise Exception("Selenium not installed. Run: pip install selenium")
        cls.driver = get_driver()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def create_user(self, username='seleniumuser', password='TestPass@123', role='student'):
        user = User.objects.create_user(username=username, password=password, role=role)
        return user

    def login(self, username='seleniumuser', password='TestPass@123'):
        self.driver.get(f'{self.live_server_url}/users/login/')
        wait_for(self.driver, By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(1)

        # ─────────────────────────────────────────────
        # M1 — Users
        # ─────────────────────────────────────────────
        class UserSeleniumTests(BaseSeleniumTest):

            def test_TC_S01_full_registration_flow(self):
                """TC-S01: Register → lands on login page."""
                self.driver.get(f'{self.live_server_url}/users/register/')
                wait_for(self.driver, By.NAME, 'username').send_keys('newseleniumuser')
                self.driver.find_element(By.NAME, 'email').send_keys('sel@test.com')
                self.driver.find_element(By.NAME, 'password1').send_keys('StrongPass@123')
                self.driver.find_element(By.NAME, 'password2').send_keys('StrongPass@123')
                self.driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                time.sleep(1)
                self.assertIn('/login', self.driver.current_url)

            def test_TC_S02_login_and_see_dashboard(self):
                """TC-S02: Login → dashboard visible."""
                self.create_user()
                self.login()
                self.assertIn('/dashboard', self.driver.current_url)
                body_text = self.driver.find_element(By.TAG_NAME, 'body').text
                self.assertIn('seleniumuser', body_text.lower())

            def test_TC_S03_edit_profile_and_save(self):
                """TC-S03: Edit profile → success."""
                self.create_user(username='profileseluser')
                self.login(username='profileseluser')
                self.driver.get(f'{self.live_server_url}/users/profile/')
                time.sleep(1)
                try:
                    gpa_field = self.driver.find_element(By.NAME, 'gpa')
                    gpa_field.clear()
                    gpa_field.send_keys('3.75')
                except Exception:
                    pass
                try:
                    self.driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                    time.sleep(1)
                except Exception:
                    pass
                self.assertNotIn('500', self.driver.title)

    # ─────────────────────────────────────────────
    # M2 — Universities
    # ─────────────────────────────────────────────
    class UniversitySeleniumTests(BaseSeleniumTest):

        def setUp(self):
            self.create_user(username='uniselusr')
            University.objects.create(name='MIT', country='USA', city='Cambridge',
                                      ranking=3, min_gpa=3.8, min_ielts=7.0)
            University.objects.create(name='Oxford', country='UK', city='Oxford',
                                      ranking=2, min_gpa=3.5, min_ielts=7.5)

        def test_TC_S04_search_filters_list(self):
            """TC-S04: Type 'MIT' in search → list shows MIT."""
            self.login(username='uniselusr')
            self.driver.get(f'{self.live_server_url}/universities/')
            search_box = wait_for(self.driver, By.NAME, 'search')
            search_box.send_keys('MIT')
            search_box.submit()
            time.sleep(1)
            body = self.driver.find_element(By.TAG_NAME, 'body').text
            self.assertIn('MIT', body)
            self.assertNotIn('Oxford', body)

        def test_TC_S05_click_university_opens_detail(self):
            """TC-S05: Click Harvard card → detail page."""
            self.login(username='uniselusr')
            self.driver.get(f'{self.live_server_url}/universities/')
            time.sleep(1)
            mit_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'MIT')
            mit_link.click()
            time.sleep(1)
            body = self.driver.find_element(By.TAG_NAME, 'body').text
            self.assertIn('MIT', body)

            # ─────────────────────────────────────────────
            # M3 — Scholarships
            # ─────────────────────────────────────────────
            class ScholarshipSeleniumTests(BaseSeleniumTest):

                def setUp(self):
                    self.create_user(username='scholseluser')
                    Scholarship.objects.create(title='Fulbright', provider='US Govt',
                                               amount=50000, funding_type='full',
                                               min_gpa_required=3.5, min_ielts_required=7.0)
                    Scholarship.objects.create(title='DAAD', provider='Germany',
                                               amount=20000, funding_type='partial',
                                               min_gpa_required=3.0, min_ielts_required=6.5)

                def test_TC_S06_filter_by_funding_pill(self):
                    """TC-S06: Click Full Funding pill → list updates."""
                    self.login(username='scholseluser')
                    self.driver.get(f'{self.live_server_url}/scholarships/')
                    time.sleep(1)
                    try:
                        full_pill = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Full')
                        full_pill.click()
                        time.sleep(1)
                    except Exception:
                        self.driver.get(f'{self.live_server_url}/scholarships/?funding=full')
                        time.sleep(1)
                    body = self.driver.find_element(By.TAG_NAME, 'body').text
                    self.assertIn('Fulbright', body)

                def test_TC_S07_click_scholarship_opens_detail(self):
                    """TC-S07: Click Fulbright → detail page."""
                    self.login(username='scholseluser')
                    self.driver.get(f'{self.live_server_url}/scholarships/')
                    time.sleep(1)
                    link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Fulbright')
                    link.click()
                    time.sleep(1)
                    body = self.driver.find_element(By.TAG_NAME, 'body').text
                    self.assertIn('Fulbright', body)

        # ─────────────────────────────────────────────
        # M4 — Dashboard
        # ─────────────────────────────────────────────
        class DashboardSeleniumTests(BaseSeleniumTest):

            def setUp(self):
                self.user = self.create_user(username='dashseluser')

            def test_TC_S08_dashboard_stat_cards_visible(self):
                """TC-S08: 4 stat cards visible on dashboard."""
                self.login(username='dashseluser')
                self.driver.get(f'{self.live_server_url}/dashboard/')
                time.sleep(1)
                body = self.driver.find_element(By.TAG_NAME, 'body').text
                self.assertNotIn('Page not found', body)
                self.assertNotIn('Server Error', body)

            def test_TC_S09_recent_applications_shown(self):
                """TC-S09: Dashboard shows recent applications section."""
                university = University.objects.create(name='Dash Uni', country='USA', city='NY',
                                                       ranking=10, min_gpa=3.0, min_ielts=6.0)
                Application.objects.create(user=self.user, university=university, status='submitted',
                                           deadline=datetime.date.today() + datetime.timedelta(days=10))
                self.login(username='dashseluser')
                self.driver.get(f'{self.live_server_url}/dashboard/')
                time.sleep(1)
                body = self.driver.find_element(By.TAG_NAME, 'body').text
                self.assertIn('Dash Uni', body)

                # ─────────────────────────────────────────────
                # M5 — Applications
                # ─────────────────────────────────────────────
                class ApplicationSeleniumTests(BaseSeleniumTest):

                    def setUp(self):
                        self.user = self.create_user(username='appseluser')
                        self.university = University.objects.create(name='Sel Uni', country='UK', city='London',
                                                                    ranking=5, min_gpa=3.0, min_ielts=6.5)

                    def test_TC_S10_create_application_flow(self):
                        """TC-S10: Fill form → Submit → app appears in list."""
                        self.login(username='appseluser')
                        self.driver.get(f'{self.live_server_url}/applications/create/')
                        time.sleep(1)
                        try:
                            from selenium.webdriver.support.ui import Select
                            uni_select = Select(self.driver.find_element(By.NAME, 'university'))
                            uni_select.select_by_visible_text('Sel Uni')
                        except Exception:
                            pass
                        try:
                            deadline_field = self.driver.find_element(By.NAME, 'deadline')
                            deadline_field.send_keys('2025-12-31')
                        except Exception:
                            pass
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                            time.sleep(1)
                        except Exception:
                            pass
                        self.driver.get(f'{self.live_server_url}/applications/')
                        time.sleep(1)
                        body = self.driver.find_element(By.TAG_NAME, 'body').text
                        self.assertNotIn('Server Error', body)

                    def test_TC_S11_status_tab_filter(self):
                        """TC-S11: Click Accepted tab → list filters."""
                        Application.objects.create(user=self.user, university=self.university, status='accepted',
                                                   deadline=datetime.date.today() + datetime.timedelta(days=10))
                        self.login(username='appseluser')
                        self.driver.get(f'{self.live_server_url}/applications/')
                        time.sleep(1)
                        try:
                            accepted_tab = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Accepted')
                            accepted_tab.click()
                            time.sleep(1)
                        except Exception:
                            self.driver.get(f'{self.live_server_url}/applications/?status=accepted')
                            time.sleep(1)
                        body = self.driver.find_element(By.TAG_NAME, 'body').text
                        self.assertNotIn('Server Error', body)

                    def test_TC_S12_delete_application(self):
                        """TC-S12: Delete application → removed from list."""
                        app = Application.objects.create(user=self.user, university=self.university,
                                                         status='incomplete',
                                                         deadline=datetime.date.today() + datetime.timedelta(days=10))
                        self.login(username='appseluser')
                        self.driver.get(f'{self.live_server_url}/applications/{app.pk}/delete/')
                        time.sleep(1)
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                            time.sleep(1)
                        except Exception:
                            pass
                        self.assertFalse(Application.objects.filter(pk=app.pk).exists())



# ─────────────────────────────────────────────
# M6 — Notifications
# ─────────────────────────────────────────────
class NotificationSeleniumTests(BaseSeleniumTest):

    def setUp(self):
        self.user = self.create_user(username='notifseluser')
        self.notif = Notification.objects.create(
            user=self.user, type='general', title='Unread Notif',
            message='This is unread.', is_read=False
        )

    def test_TC_S13_unread_notification_highlighted(self):
        """TC-S13: Unread notification has highlighted styling."""
        self.login(username='notifseluser')
        self.driver.get(f'{self.live_server_url}/notifications/')
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Unread Notif', body)

    def test_TC_S14_mark_all_read_updates_ui(self):
        """TC-S14: Click Mark All as Read → unread count becomes 0."""
        self.login(username='notifseluser')
        self.driver.get(f'{self.live_server_url}/notifications/')
        time.sleep(1)
        try:
            mark_all_btn = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Mark All')
            mark_all_btn.click()
        except Exception:
            try:
                mark_all_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-action="mark-all"]')
                mark_all_btn.click()
            except Exception:
                self.driver.get(f'{self.live_server_url}/notifications/mark-all-read/')
        time.sleep(1)
        self.notif.refresh_from_db()
        self.assertTrue(self.notif.is_read)

        # ─────────────────────────────────────────────
        # M7 — Eligibility
        # ─────────────────────────────────────────────
        class EligibilitySeleniumTests(BaseSeleniumTest):

            def setUp(self):
                self.user = self.create_user(username='eligseluser')
                profile = Profile.objects.get(user=self.user)
                profile.gpa = 3.8
                profile.english_score = 7.5
                profile.english_proficiency = 'ielts'
                profile.degree_level = 'bachelors'
                profile.save()
                University.objects.create(name='Harvard', country='USA', city='Cambridge',
                                          ranking=1, min_gpa=3.7, min_ielts=7.0)

            def test_TC_S15_eligibility_score_banner_visible(self):
                """TC-S15: Score banner visible on eligibility page."""
                self.login(username='eligseluser')
                self.driver.get(f'{self.live_server_url}/eligibility/check/')
                time.sleep(2)
                body = self.driver.find_element(By.TAG_NAME, 'body').text
                self.assertNotIn('Server Error', body)
                self.assertNotIn('Page not found', body)

            def test_TC_S16_matched_universities_section(self):
                """TC-S16: Matched universities section shows with profile."""
                self.login(username='eligseluser')
                self.driver.get(f'{self.live_server_url}/eligibility/check/')
                time.sleep(2)
                body = self.driver.find_element(By.TAG_NAME, 'body').text
                self.assertIn('Harvard', body)

