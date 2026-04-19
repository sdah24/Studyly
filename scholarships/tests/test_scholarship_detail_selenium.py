from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipDetailSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(

            name="Cambridge",

            country="UK"

        )

        self.scholarship = Scholarship.objects.create(

            title="Cambridge Scholarship",

            description="Test",

            amount=9000,

            deadline="2030-01-01",

            university=university

        )

    def tearDown(self):

        self.browser.quit()

    def test_detail_page_opens(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/detail/{self.scholarship.id}/"

        )

        page = self.browser.page_source

        assert "Cambridge Scholarship" in page