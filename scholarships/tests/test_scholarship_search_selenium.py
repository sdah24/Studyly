from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipSearchSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(

            name="MIT",

            country="USA"

        )

        Scholarship.objects.create(

            title="MIT Scholarship",

            description="Test",

            amount=6000,

            deadline="2030-01-01",

            university=university

        )

    def tearDown(self):

        self.browser.quit()

    def test_search_functionality(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/search/"

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

        assert "MIT Scholarship" in page
