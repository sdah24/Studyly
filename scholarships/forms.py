from django import forms

from .models import Scholarship


class ScholarshipForm(forms.ModelForm):

    class Meta:

        model = Scholarship

        fields = [

            "title",
            "description",
            "amount",
            "deadline",
            "university",

        ]

        widgets = {

            "deadline":
                forms.DateInput(
                    attrs={"type": "date"}
                ),

            "description":
                forms.Textarea(
                    attrs={"rows": 4}
                ),

        }