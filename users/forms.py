# users/forms.py

from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "full_name",
            "phone_number",
            "date_of_birth",
            "address",
        ]

        widgets = {

            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),

            "address": forms.Textarea(
                attrs={"rows": 3}
            ),
        }