from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Scholarship


@login_required
def scholarship_list(request):
    scholarships = Scholarship.objects.all()

    # Search
    query = request.GET.get('q', '')
    if query:
        scholarships = scholarships.filter(
            Q(title__icontains=query) |
            Q(provider__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter pill
    funding_filter = request.GET.get('funding', '')
    if funding_filter == 'full':
        scholarships = scholarships.filter(funding_type='full')
    elif funding_filter == 'partial':
        scholarships = scholarships.filter(funding_type='partial')
    elif funding_filter == 'open':
        scholarships = scholarships.filter(deadline__gte=timezone.now().date())

    total = scholarships.count()

    return render(request, 'scholarships/scholarships.html', {
        'scholarships': scholarships,
        'total': total,
        'query': query,
        'funding_filter': funding_filter,
    })


@login_required
def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)

    return render(request, 'scholarships/scholarship_detail.html', {
        'scholarship': scholarship,
    })