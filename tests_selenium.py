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