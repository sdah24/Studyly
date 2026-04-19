from django import forms


class UniversitySearchForm(forms.Form):

    query = forms.CharField(

        max_length=255,

        required=False,

        label="Search",

        widget=forms.TextInput(

            attrs={

                "placeholder":
                "Search universities...",

                "class":
                "form-control",

                "name":
                "query",

            }

        )

    )