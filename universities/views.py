from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import University


@login_required
def university_list(request):
    universities = University.objects.all()

    # Search
    query = request.GET.get('q', '')
    if query:
        universities = universities.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query)
        )

    # Country filter pill
    country_filter = request.GET.get('country', '')
    if country_filter == 'usa':
        universities = universities.filter(country__icontains='USA')
    elif country_filter == 'uk':
        universities = universities.filter(country__icontains='UK')
    elif country_filter == 'europe':
        universities = universities.filter(
            Q(country__icontains='Germany') |
            Q(country__icontains='France') |
            Q(country__icontains='Switzerland') |
            Q(country__icontains='Netherlands')
        )
    elif country_filter == 'top':
        universities = universities.filter(ranking__lte=20)

    total = universities.count()

    return render(request, 'universities/universities.html', {
        'universities': universities,
        'total': total,
        'query': query,
        'country_filter': country_filter,
    })


@login_required
def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    programs = university.programs.all()
    scholarships = university.scholarships.all()

    return render(request, 'universities/university_detail.html', {
        'university': university,
        'programs': programs,
        'scholarships': scholarships,
    })