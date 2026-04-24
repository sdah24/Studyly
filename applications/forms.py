from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [
            'university', 'program', 'deadline', 'notes',
            'personal_statement', 'transcripts', 'recommendations',
            'english_test', 'financial_docs', 'cv_resume',
        ]
        # NOTE: 'status' is intentionally excluded — set automatically by model.save()
        widgets = {
            'university': forms.Select(attrs={'class': 'form-select'}),
            'program':    forms.Select(attrs={'class': 'form-select'}),
            'deadline':   forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'notes':      forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Any notes about this application…'
            }),
            # File fields — accept PDF and common image types
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
        self.fields['program'].empty_label    = '— Select a Program (optional) —'
        self.fields['program'].required       = False
        self.fields['deadline'].required      = False
        self.fields['notes'].required         = False
        # All document fields are optional individually
        for doc_field in ['personal_statement', 'transcripts', 'recommendations',
                          'english_test', 'financial_docs', 'cv_resume']:
            self.fields[doc_field].required = False