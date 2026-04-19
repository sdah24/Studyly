# users/tests/test_profile_selenium.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from django.contrib.auth.models import User


class ProfileSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        self.user = User.objects.create_user(
            username="seleniumuser",
            password="password123"
        )

    def tearDown(self):
        self.browser.quit()

    def test_profile_creation(self):

        self.browser.get(
            f"{self.live_server_url}/accounts/login/"
        )

        self.browser.find_element(
            By.NAME,
            "username"
        ).send_keys("seleniumuser")

        self.browser.find_element(
            By.NAME,
            "password"
        ).send_keys("password123")

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        self.browser.get(
            f"{self.live_server_url}/profile/create/"
        )

        self.browser.find_element(
            By.NAME,
            "full_name"
        ).send_keys("Selenium User")

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()