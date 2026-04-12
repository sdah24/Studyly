from django.shortcuts import render

from universities.models import University
# Create your views here.


def universities_view(request):

        universities =  University.objects.all()

        return render(request, "universities/universities.html",{"universities": universities}
                      )

