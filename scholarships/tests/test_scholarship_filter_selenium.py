from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipFilterSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(

            name="MIT",

            country="USA"

        )

        Scholarship.objects.create(

            title="MIT Grant",

            description="Test",

            amount=6000,

            deadline="2030-01-01",

            university=university

        )

    def tearDown(self):

        self.browser.quit()

    def test_filter_search(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/search/"

        )

        search_box = self.browser.find_element(
            By.NAME,
            "query"
        )

        search_box.send_keys("MIT")

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        page = self.browser.page_source

        assert "MIT Grant" in page