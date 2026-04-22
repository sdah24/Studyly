from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user extending Django's AbstractUser.
    AbstractUser already provides: username, email, password,
    first_name, last_name, is_staff, is_active, date_joined, etc.
    We add role so we can distinguish student / admin / consultant.
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('consultant', 'Educational Consultant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

    # Convenience helpers
    def is_student(self):
        return self.role == 'student'

    def is_admin_user(self):
        return self.role == 'admin'

    def is_consultant(self):
        return self.role == 'consultant'


class Profile(models.Model):
    """
    Extended academic/personal profile for a student.
    Created automatically via signal when a User is saved.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Personal
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True
    )

    # Academic (used by Eligibility module)
    GPA = models.FloatField(null=True, blank=True)
    degree_level = models.CharField(
        max_length=50,
        choices=[
            ('bachelor', "Bachelor's"),
            ('master', "Master's"),
            ('phd', 'PhD'),
        ],
        blank=True,
        null=True
    )
    english_proficiency = models.CharField(
        max_length=50,
        choices=[
            ('ielts', 'IELTS'),
            ('toefl', 'TOEFL'),
            ('none', 'None'),
        ],
        blank=True,
        null=True
    )
    english_score = models.FloatField(null=True, blank=True)
    work_experience_years = models.IntegerField(default=0)

    # Preferences (used by search/eligibility)
    preferred_countries = models.CharField(max_length=255, blank=True, null=True)
    budget = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def preferred_countries_list(self):
        """Returns preferred_countries as a Python list."""
        if self.preferred_countries:
            return [c.strip() for c in self.preferred_countries.split(',')]
        return []