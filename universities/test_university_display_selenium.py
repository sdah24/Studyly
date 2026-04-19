from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

from universities.models import University


class UniversityDisplayTest(
    StaticLiveServerTestCase
):

    def setUp(self):

        self.browser = webdriver.Chrome()

        University.objects.create(
            name="Stanford University",
            country="USA"
        )

    def tearDown(self):

        self.browser.quit()

    def test_university_visible(self):

        self.browser.get(

            f"{self.live_server_url}/universities/"

        )

        page = self.browser.page_source

        assert "Stanford University" in page