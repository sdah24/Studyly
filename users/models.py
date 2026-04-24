from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user extending Django's AbstractUser.
    AbstractUser already provides: username, email, password,
    first_name, last_name, is_staff, is_active, date_joined, etc.
    Role is now selectable by the user on registration (student / consultant).
    Admin is reserved for staff only.
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

    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)


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


class Message(models.Model):
    """
    Direct message between two users.
    Supports any user ↔ user conversation (student ↔ student,
    student ↔ consultant, consultant ↔ consultant, etc.)
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender} → {self.recipient} at {self.created_at:%Y-%m-%d %H:%M}"

    @classmethod
    def get_conversation(cls, user_a, user_b):
        """Return all messages exchanged between two users, ordered by time."""
        return cls.objects.filter(
            sender__in=[user_a, user_b],
            recipient__in=[user_a, user_b]
        ).order_by('created_at')

    @classmethod
    def get_inbox_threads(cls, user):
        """
        Return a list of dicts, one per unique conversation partner,
        with the latest message and unread count.
        """
        from django.db.models import Q, Max
        partners_qs = (
            cls.objects
            .filter(Q(sender=user) | Q(recipient=user))
            .values_list('sender_id', 'recipient_id')
        )
        partner_ids = set()
        for s, r in partners_qs:
            other = r if s == user.pk else s
            partner_ids.add(other)

        threads = []
        for pid in partner_ids:
            other_user = User.objects.get(pk=pid)
            last_msg = (
                cls.objects
                .filter(
                    Q(sender=user, recipient=other_user) |
                    Q(sender=other_user, recipient=user)
                )
                .order_by('-created_at')
                .first()
            )
            unread = cls.objects.filter(
                sender=other_user, recipient=user, is_read=False
            ).count()
            threads.append({
                'partner': other_user,
                'last_message': last_msg,
                'unread_count': unread,
            })

        # Sort threads: most recent first
        threads.sort(key=lambda t: t['last_message'].created_at, reverse=True)
        return threads