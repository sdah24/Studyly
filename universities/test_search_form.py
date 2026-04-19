from django.test import TestCase

from universities.forms import UniversitySearchForm


class UniversitySearchFormTest(
    TestCase
):

    def test_form_valid_input(self):

        form = UniversitySearchForm(

            data={

                "query":
                "Harvard"

            }

        )

        self.assertTrue(

            form.is_valid()

        )

    def test_form_empty_input(self):

        form = UniversitySearchForm(

            data={

                "query":
                ""

            }

        )

        self.assertTrue(

            form.is_valid()

        )