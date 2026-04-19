from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University
from scholarships.models import Scholarship


class EditScholarshipSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(

            name="Oxford",
            country="UK"

        )

        self.scholarship = Scholarship.objects.create(

            title="Old Scholarship",

            description="Test",

            amount=1000,

            deadline="2030-01-01",

            university=university

        )

    def tearDown(self):

        self.browser.quit()

    def test_edit_scholarship(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/edit/{self.scholarship.id}/"

        )

        title_field = self.browser.find_element(
            By.NAME,
            "title"
        )

        title_field.clear()

        title_field.send_keys(
            "Updated Scholarship"
        )

        self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        page = self.browser.page_source

        assert "Scholarship" in page