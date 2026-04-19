from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University


class AddScholarshipSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        self.university = University.objects.create(

            name="Oxford",
            country="UK"

        )

    def tearDown(self):

        self.browser.quit()

    def test_add_scholarship(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/add/"

        )

        self.browser.find_element(
            By.NAME,
            "title"
        ).send_keys("Scholarship Test")

        self.browser.find_element(
            By.NAME,
            "amount"
        ).send_keys("1000")

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        page = self.browser.page_source

        assert "Scholarship" in page