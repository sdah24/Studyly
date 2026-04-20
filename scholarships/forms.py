from django import forms

from universities.models import University


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

    university = forms.ModelChoiceField(

        queryset=University.objects.all(),

        required=False,

        empty_label="All Universities",

        widget=forms.Select(

            attrs={

                "class": "form-control"

            }

        )

    )

    min_amount = forms.DecimalField(

        required=False,

        label="Minimum Amount",

        widget=forms.NumberInput(

            attrs={

                "class": "form-control",

                "placeholder":
                "Minimum Amount"

            }

        )

    )

    deadline_before = forms.DateField(

        required=False,

        widget=forms.DateInput(

            attrs={

                "type": "date",

                "class": "form-control"

            }

        )

    )