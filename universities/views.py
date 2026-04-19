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
    form = UniversitySearchForm(request.GET or None)
    universities = University.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            universities = universities.filter(
                name__icontains=query
            )

    paginator = Paginator(universities, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
        "universities": page_obj,
    }

    return render(
        request,
        "universities/university_search.html",
        context
    )