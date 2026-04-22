from django import forms
from universities.models import University


CATEGORY_CHOICES = [

    ("", "All Categories"),
    ("merit", "Merit-Based"),
    ("need", "Need-Based"),
    ("sports", "Sports"),
    ("research", "Research"),

]


class ScholarshipSearchForm(forms.Form):

    query = forms.CharField(

        max_length=255,
        required=False,

        widget=forms.TextInput(
            attrs={
                "placeholder": "Search scholarships...",
                "class": "search-input"
            }
        )

    )

    university = forms.ModelChoiceField(

        queryset=University.objects.all(),
        required=False,
        empty_label="All Universities",

        widget=forms.Select(
            attrs={
                "class": "filter-select"
            }
        )

    )

    category = forms.ChoiceField(

        choices=CATEGORY_CHOICES,
        required=False,

        widget=forms.Select(
            attrs={
                "class": "filter-select"
            }
        )

    )

    min_amount = forms.DecimalField(

        required=False,

        widget=forms.NumberInput(
            attrs={
                "placeholder": "Minimum Amount",
                "class": "filter-input"
            }
        )

    )

    deadline_before = forms.DateField(

        required=False,

        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "filter-input"
            }
        )

    )