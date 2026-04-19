from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class ScholarshipSearchUISeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):

        self.browser.quit()

    def test_ui_loads(self):

        self.browser.get(

            f"{self.live_server_url}/scholarships/search/"

        )

        page = self.browser.page_source

        assert "Scholarship Search" in page