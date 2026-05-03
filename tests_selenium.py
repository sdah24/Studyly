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