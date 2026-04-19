from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By


class UniversitySearchInputTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):

        self.browser.quit()

    def test_search_input_exists(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        search_input = self.browser.find_element(

            By.NAME,

            "query"

        )

        assert search_input is not None