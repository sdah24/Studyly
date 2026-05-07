from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Scholarship

# Common aliases for country names as stored in preferred_countries
COUNTRY_ALIASES = {
    'usa':           ['united states', 'u.s.', 'u.s.a', 'american', 'america'],
    'uk':            ['united kingdom', 'u.k.', 'britain', 'british', 'england', 'great britain'],
    'australia':     ['australian'],
    'canada':        ['canadian'],
    'germany':       ['german', 'deutschland', 'daad'],
    'france':        ['french'],
    'japan':         ['japanese', 'jasso'],
    'china':         ['chinese', 'csc'],
    'new zealand':   ['new zealander', 'nz'],
    'netherlands':   ['dutch', 'holland'],
    'sweden':        ['swedish'],
    'norway':        ['norwegian'],
    'switzerland':   ['swiss'],
    'europe':        ['european', 'erasmus', 'eu '],
    'commonwealth':  ['commonwealth secretariat'],
}


def _country_terms(preferred_country):
    """Return all search terms for a given preferred country string."""
    key = preferred_country.lower().strip()
    terms = [key]
    for canon, aliases in COUNTRY_ALIASES.items():
        if key == canon or key in aliases:
            terms.append(canon)
            terms.extend(aliases)
            break
    if key in COUNTRY_ALIASES:
        terms.extend(COUNTRY_ALIASES[key])
    return list(set(terms))


def _scholarship_text(s):
    """All searchable text fields on a scholarship (lowercased)."""
    parts = [s.title, s.provider]
    if s.university:
        parts.extend([s.university.country or '', s.university.name or ''])
    return ' '.join(parts).lower()


def _is_match(s, preferred):
    """Return True if scholarship matches any preferred country."""
    for p in preferred:
        terms = _country_terms(p)
        text = _scholarship_text(s)
        if any(t in text for t in terms):
            return True
    return False


@login_required
def scholarship_list(request):
    scholarships = Scholarship.objects.select_related('university').all()

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
        preferred = profile.preferred_countries_list()
    except Exception:
        pass

    matched = []
    others = []
    if preferred:
        for s in scholarships:
            if _is_match(s, preferred):
                matched.append(s)
            else:
                others.append(s)
    else:
        others = list(scholarships)

    total = len(matched) + len(others)

    return render(request, 'scholarships/scholarships.html', {
        'matched':             matched,
        'others':              others,
        'scholarships':        matched + others,
        'total':               total,
        'query':               query,
        'funding_filter':      funding_filter,
        'has_preferred':       bool(preferred),
        'preferred_countries': ', '.join(preferred),
    })


@login_required
def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    return render(request, 'scholarships/scholarship_detail.html', {
        'scholarship': scholarship,
    })