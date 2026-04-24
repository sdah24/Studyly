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

    # ── Document uploads (replaces old BooleanFields) ──────────────────────────
    personal_statement = models.FileField(
        upload_to='applications/personal_statements/',
        null=True, blank=True
    )
    transcripts = models.FileField(
        upload_to='applications/transcripts/',
        null=True, blank=True
    )
    recommendations = models.FileField(
        upload_to='applications/recommendations/',
        null=True, blank=True
    )
    english_test = models.FileField(
        upload_to='applications/english_tests/',
        null=True, blank=True
    )
    financial_docs = models.FileField(
        upload_to='applications/financial_docs/',
        null=True, blank=True
    )
    cv_resume = models.FileField(
        upload_to='applications/cv_resumes/',
        null=True, blank=True
    )

    notes    = models.TextField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)

    applied_date = models.DateField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']
        unique_together = ['user', 'university', 'program']

    def __str__(self):
        return f"{self.user.username} → {self.university.name}"

    # ── Document helpers ───────────────────────────────────────────────────────
    def documents_submitted(self):
        """Count how many of the 6 documents have been uploaded."""
        fields = [
            self.personal_statement,
            self.transcripts,
            self.recommendations,
            self.english_test,
            self.financial_docs,
            self.cv_resume,
        ]
        return sum(1 for f in fields if f)

    def total_documents(self):
        return 6

    def progress_percent(self):
        return int((self.documents_submitted() / self.total_documents()) * 100)

    def all_documents_uploaded(self):
        return self.documents_submitted() == self.total_documents()

    # ── Auto-status logic ──────────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        # Only auto-set status if admin hasn't manually set under_review/accepted/rejected
        if self.status in ('incomplete', 'submitted'):
            if self.all_documents_uploaded():
                self.status = 'submitted'
            else:
                self.status = 'incomplete'
        super().save(*args, **kwargs)

    # ── UI helpers ─────────────────────────────────────────────────────────────
    def status_color(self):
        return {
            'incomplete':   {'bg': '#fff7ed', 'color': '#c2410c'},
            'submitted':    {'bg': '#dbeafe', 'color': '#1d4ed8'},
            'under_review': {'bg': '#fffbeb', 'color': '#a16207'},
            'accepted':     {'bg': '#f0fdf4', 'color': '#15803d'},
            'rejected':     {'bg': '#fef2f2', 'color': '#b91c1c'},
        }.get(self.status, {'bg': '#f3f4f6', 'color': '#374151'})

    def doc_filename(self, field):
        """Return just the filename (not full path) for display."""
        import os
        if field:
            return os.path.basename(field.name)
        return None