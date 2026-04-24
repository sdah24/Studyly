# In your users/forms.py, update RegisterForm to include the role field.
# Only 'student' and 'consultant' are offered — 'admin' stays staff-only.

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


REGISTER_ROLE_CHOICES = [
    ('student',    '🎓  Student – Looking for universities'),
    ('consultant', '🧑‍💼  Consultant – Guiding students abroad'),
]


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=REGISTER_ROLE_CHOICES,
        initial='student',
        widget=forms.RadioSelect,   # rendered as cards in the template via hidden radios
        required=True,
    )

    class Meta:
        model = User
        # List all fields you want in the registration form.
        # 'role' is included so the form validates and saves it.
        fields = ['first_name', 'last_name', 'username', 'email',
                  'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']   # explicitly set the role
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Standard auth form — no changes needed."""
    pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']