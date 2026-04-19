from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class UniversitySearchUISeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):

        self.browser.quit()

    def test_search_page_ui_loads(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        page = self.browser.page_source

        assert "University Search" in page