from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University
from scholarships.models import Scholarship


class DeleteScholarshipSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(
            name="Test University",
            country="USA"
        )

        self.scholarship = Scholarship.objects.create(
            title="Delete Scholarship",
            description="Test",
            amount=2000,
            deadline="2030-01-01",
            university=university
        )

    def tearDown(self):

        self.browser.quit()

    def test_delete_scholarship(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/delete/{self.scholarship.id}/"

        )

        delete_button = self.browser.find_element(
            By.XPATH,
            "//button[@type='submit']"
        )

        delete_button.click()

        page = self.browser.page_source

        assert "Scholarship" in page