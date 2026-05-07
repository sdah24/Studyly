from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import University, Program


@login_required
def university_list(request):
    universities = University.objects.all()

    query = request.GET.get('q', '')
    if query:
        universities = universities.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query)
        )

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


@login_required
def university_programs(request, pk):
    university = get_object_or_404(University, pk=pk)
    programs = university.programs.all().order_by('name')

    # Optional degree-level filter passed from the form
    level = request.GET.get('level', '').strip()
    if level:
        programs = programs.filter(level=level)

    data = [
        {
            'id': p.pk,
            'name': p.name,
            'level': p.level,
            'level_display': p.get_level_display(),
        }
        for p in programs
    ]
    return JsonResponse({'programs': data})