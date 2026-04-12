from django.shortcuts import render

from universities.models import University
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

