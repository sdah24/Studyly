from django.shortcuts import render


def scholarship_search(request):

    return render(

        request,

        "scholarships/scholarship_search.html"

    )