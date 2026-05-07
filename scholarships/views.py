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

    # ── Country match ──────────────────────────────────────────────
    preferred = []
    try:
        profile = request.user.profile
        preferred = profile.preferred_countries_list()  # returns a list
    except Exception:
        pass

    matched = []
    others = []
    if preferred:
        for s in scholarships:
            # Primary: match via linked university's country
            country = s.university.country if s.university else None
            country_match = country and any(
                p.lower() in country.lower() or country.lower() in p.lower()
                for p in preferred
            )

            # Fallback: match via scholarship title or provider text
            text_match = not country_match and any(
                p.lower() in s.title.lower() or p.lower() in s.provider.lower()
                for p in preferred
            )

            if country_match or text_match:
                matched.append(s)
            else:
                others.append(s)
    else:
        others = list(scholarships)

    total = len(matched) + len(others)

    return render(request, 'scholarships/scholarships.html', {
        'matched':           matched,
        'others':            others,
        'scholarships':      matched + others,  # kept for total count
        'total':             total,
        'query':             query,
        'funding_filter':    funding_filter,
        'has_preferred':     bool(preferred),
        'preferred_countries': ', '.join(preferred),
    })


@login_required
def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    return render(request, 'scholarships/scholarship_detail.html', {
        'scholarship': scholarship,
    })