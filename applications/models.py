from django.db import models
from django.conf import settings
from universities.models import University, Program


class Application(models.Model):

    STATUS_CHOICES = [
        ('incomplete',   'Incomplete'),
        ('submitted',    'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted',     'Accepted'),
        ('rejected',     'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='applications'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='incomplete'
    )

    # Progress tracking
    personal_statement  = models.BooleanField(default=False)
    transcripts         = models.BooleanField(default=False)
    recommendations     = models.BooleanField(default=False)
    english_test        = models.BooleanField(default=False)
    financial_docs      = models.BooleanField(default=False)
    cv_resume           = models.BooleanField(default=False)

    notes    = models.TextField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)

    applied_date = models.DateField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']
        unique_together = ['user', 'university', 'program']

    def __str__(self):
        return f"{self.user.username} → {self.university.name}"

    def documents_submitted(self):
        fields = [
            self.personal_statement, self.transcripts,
            self.recommendations, self.english_test,
            self.financial_docs, self.cv_resume,
        ]
        return sum(fields)

    def total_documents(self):
        return 6

    def progress_percent(self):
        return int((self.documents_submitted() / self.total_documents()) * 100)

    def status_color(self):
        return {
            'incomplete':   {'bg': '#fff7ed', 'color': '#c2410c'},
            'submitted':    {'bg': '#dbeafe', 'color': '#1d4ed8'},
            'under_review': {'bg': '#fffbeb', 'color': '#a16207'},
            'accepted':     {'bg': '#f0fdf4', 'color': '#15803d'},
            'rejected':     {'bg': '#fef2f2', 'color': '#b91c1c'},
        }.get(self.status, {'bg': '#f3f4f6', 'color': '#374151'})