from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University


class UniversityResultSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        University.objects.create(

            name="Cambridge University",

            country="UK"

        )

    def tearDown(self):

        self.browser.quit()

    def test_result_visible(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        page = self.browser.page_source

        assert "Cambridge University" in page