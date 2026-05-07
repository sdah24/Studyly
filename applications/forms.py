from django import forms
from .models import Application
from universities.models import Program


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [
    'university', 'program', 'intake_season', 'deadline', 'notes',
            'personal_statement', 'transcripts', 'recommendations',
            'english_test', 'financial_docs', 'cv_resume',
        ]
        widgets = {
            'university': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_university',
            }),
            'program': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_program',
            }),
            'intake_season': forms.Select(attrs={'class': 'form-select'}),
'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Any notes about this application…'
            }),
            'personal_statement': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.jpg,.png', 'class': 'file-input'}),
            'transcripts':        forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png',            'class': 'file-input'}),
            'recommendations':    forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.jpg,.png', 'class': 'file-input'}),
            'english_test':       forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png',            'class': 'file-input'}),
            'financial_docs':     forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png',            'class': 'file-input'}),
            'cv_resume':          forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx',           'class': 'file-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['university'].empty_label = '— Select a University —'
        self.fields['program'].empty_label = '— Select a Program —'
        self.fields['program'].required = True
        self.fields['deadline'].required = False
        self.fields['notes'].required = False

        for doc_field in ['personal_statement', 'transcripts', 'recommendations',
                          'english_test', 'financial_docs', 'cv_resume']:
            self.fields[doc_field].required = False

        # If editing an existing application, show only that university's programs
        if self.instance and self.instance.pk and self.instance.university_id:
            self.fields['program'].queryset = Program.objects.filter(
                university=self.instance.university
            ).order_by('name')
        else:
            # New application — start with empty program list, JS will populate it
            self.fields['program'].queryset = Program.objects.none()