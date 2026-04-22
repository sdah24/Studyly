from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import University
from .forms import UniversitySearchForm


def universities_view(request):
    universities = University.objects.all()
    return render(
        request,
        "universities/universities.html",
        {"universities": universities}
    )


def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    return render(
        request,
        "universities/university_detail.html",
        {"university": university}
    )


def university_search(request):

    form = UniversitySearchForm(
        request.GET or None
    )

    universities = University.objects.all()

    # Search
    query = request.GET.get("query")

    if query:
        universities = universities.filter(
            name__icontains=query
        )

    # Country filter (for pills)
    country = request.GET.get("country")

    if country:
        universities = universities.filter(
            country__icontains=country
        )

    # Pagination
    paginator = Paginator(
        universities,
        9
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        "form": form,
        "universities": page_obj,
        "page_obj": page_obj,

    }

    return render(

        request,
        "universities/universities.html",
        context

    )