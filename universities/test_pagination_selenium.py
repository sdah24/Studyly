from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from universities.models import University


class UniversityPaginationSeleniumTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        for i in range(25):

            University.objects.create(
                name=f"University {i}",
                country="USA"
            )

    def tearDown(self):

        self.browser.quit()

    def test_pagination_next_page(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        next_button = self.browser.find_element(

            By.LINK_TEXT,

            "Next"

        )

        next_button.click()

        page = self.browser.page_source

        assert "Page 2" in page