from django import forms
from .models import Application
from universities.models import University, Program


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'university', 'program', 'status', 'deadline',
            'personal_statement', 'transcripts', 'recommendations',
            'english_test', 'financial_docs', 'cv_resume', 'notes',
        ]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.none()
        if 'university' in self.data:
            try:
                uni_id = int(self.data.get('university'))
                self.fields['program'].queryset = Program.objects.filter(
                    university_id=uni_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.university:
            self.fields['program'].queryset = Program.objects.filter(
                university=self.instance.university
            )


class ApplicationStatusForm(forms.ModelForm):
    """Lightweight form just for updating status."""
    class Meta:
        model = Application
        fields = ['status']