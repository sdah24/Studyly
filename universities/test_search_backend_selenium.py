from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University


class UniversitySearchBackendSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        University.objects.create(
            name="MIT"
        )

    def tearDown(self):

        self.browser.quit()

    def test_search_functionality(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        self.browser.find_element(
            By.NAME,
            "query"
        ).send_keys("MIT")

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        page = self.browser.page_source

        assert "MIT" in page