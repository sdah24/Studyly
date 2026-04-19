from django import forms


class ScholarshipSearchForm(forms.Form):

    query = forms.CharField(

        max_length=255,

        required=False,

        label="Search",

        widget=forms.TextInput(

            attrs={

                "placeholder":
                "Search scholarships...",

                "class":
                "form-control",

            }

        )

    )