from django.shortcuts import render

from .models import University
from .forms import UniversitySearchForm
# Create your views here.


def universities_view(request):

        universities =  University.objects.all()

        search_query = request.GET.get("search")
        country_query = request.GET.get("country")

        # Search by name
        if search_query:
            universities = universities.filter(
                name__icontains=search_query
            )

        # Search by country
        if country_query:
            universities = universities.filter(
                country__icontains=country_query
            )

        return render(request, "universities/universities.html",{"universities": universities}
                      )


def university_search(request):

    form = UniversitySearchForm(
        request.GET or None
    )

    universities = University.objects.all()

    if form.is_valid():

        query = form.cleaned_data.get(
            "query"
        )

        if query:

            universities = universities.filter(

                name__icontains=query

            )

    context = {

        "form": form,

        "universities": universities

    }

    return render(

        request,

        "universities/university_search.html",

        context

    )











