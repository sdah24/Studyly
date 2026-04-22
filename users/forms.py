from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'student'   # default role on public registration
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Thin wrapper — just customises widget attrs for styling."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'date_of_birth', 'address',
            'GPA', 'degree_level', 'english_proficiency',
            'english_score', 'work_experience_years',
            'preferred_countries', 'budget',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'preferred_countries': forms.TextInput(
                attrs={'placeholder': 'e.g. USA, UK, Germany'}
            ),
        }