from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

from universities.models import University
from scholarships.models import Scholarship


class ScholarshipDisplaySeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        university = University.objects.create(

            name="Oxford",

            country="UK"

        )

        Scholarship.objects.create(

            title="Oxford Scholarship",

            description="Test",

            amount=1000,

            deadline="2030-01-01",

            university=university

        )

    def tearDown(self):

        self.browser.quit()

    def test_scholarship_visible(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/search/"

        )

        page = self.browser.page_source

        assert "Oxford Scholarship" in page