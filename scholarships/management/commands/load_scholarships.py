from django.core.management.base import BaseCommand
from scholarships.models import Scholarship
import datetime


SCHOLARSHIPS = [
    {
        'title': 'Fulbright Foreign Student Program',
        'provider': 'U.S. Department of State',
        'description': 'The Fulbright Program is the U.S. government flagship international exchange program. It provides funding for students, scholars, and professionals to undertake graduate study, advanced research, and university teaching.',
        'funding_type': 'full',
        'category': 'merit',
        'amount_display': 'Full Tuition + Living Expenses',
        'deadline': datetime.date(2026, 10, 15),
        'target_group': 'Graduate Students',
        'recipients_per_year': '4,000',
        'min_gpa_required': 3.0,
        'min_ielts_required': 7.0,
    },
    {
        'title': 'Chevening Scholarships',
        'provider': 'UK Government',
        'description': 'Chevening is the UK government global scholarship programme funded by the Foreign, Commonwealth and Development Office and partner organisations. It offers full financial support to study any master\'s course at any UK university.',
        'funding_type': 'full',
        'category': 'merit',
        'amount_display': '£18,000 – £30,000',
        'deadline': datetime.date(2026, 11, 2),
        'target_group': "Master's Students",
        'recipients_per_year': '1,500',
        'min_gpa_required': 3.0,
        'min_ielts_required': 6.5,
    },
    {
        'title': 'DAAD Scholarships',
        'provider': 'German Academic Exchange Service',
        'description': 'The DAAD is the world\'s largest funding organisation for the international exchange of students and researchers. It supports the internationalisation of German universities and promotes international academic exchange.',
        'funding_type': 'partial',
        'category': 'merit',
        'amount_display': '€861/month + Benefits',
        'deadline': datetime.date(2026, 12, 1),
        'target_group': 'Graduate & Postgraduate',
        'recipients_per_year': '100,000',
        'min_gpa_required': 2.5,
        'min_ielts_required': 6.0,
    },
    {
        'title': 'Australia Awards',
        'provider': 'Australian Government',
        'description': 'Australia Awards are prestigious international scholarships and short courses funded by the Australian Government. They offer opportunities for people from developing countries to undertake study, research and professional development in Australia.',
        'funding_type': 'full',
        'category': 'need',
        'amount_display': 'Full Tuition + AUD 3,000/month',
        'deadline': datetime.date(2026, 4, 30),
        'target_group': 'Developing Countries',
        'recipients_per_year': '3,000',
        'min_gpa_required': 2.8,
        'min_ielts_required': 6.5,
    },
    {
        'title': 'Erasmus Mundus Joint Masters',
        'provider': 'European Commission',
        'description': 'Erasmus Mundus Joint Master Degrees are integrated international study programmes at masters level that bring together a consortium of higher education institutions from different countries.',
        'funding_type': 'full',
        'category': 'merit',
        'amount_display': '€1,400/month + Tuition',
        'deadline': datetime.date(2027, 1, 15),
        'target_group': "Master's Students",
        'recipients_per_year': '25,000',
        'min_gpa_required': 3.0,
        'min_ielts_required': 6.5,
    },
    {
        'title': 'Commonwealth Scholarships',
        'provider': 'Commonwealth Secretariat',
        'description': 'Commonwealth Scholarships are offered to citizens of Commonwealth countries for postgraduate study in the UK. They are funded by the UK Department for International Development and administered by the Commonwealth Scholarship Commission.',
        'funding_type': 'full',
        'category': 'merit',
        'amount_display': 'Full Tuition + Stipend',
        'deadline': datetime.date(2026, 12, 15),
        'target_group': 'Commonwealth Citizens',
        'recipients_per_year': '800',
        'min_gpa_required': 3.2,
        'min_ielts_required': 7.0,
    },
]


class Command(BaseCommand):
    help = 'Load sample scholarship data into the database'

    def handle(self, *args, **kwargs):
        for data in SCHOLARSHIPS:
            scholarship, created = Scholarship.objects.update_or_create(
                title=data['title'],
                defaults=data
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status}: {scholarship.title}'))

        self.stdout.write(self.style.SUCCESS('Done loading scholarships!'))