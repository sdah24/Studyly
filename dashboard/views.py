from django.shortcuts import render, redirect
from users.models import User

def dashboard_view(request):

    return render(
        request,
        "dashboard/dashboard.html"
    )


def profile_view(request):

    if request.method == "POST":

        GPA = request.POST.get("GPA")
        budget = request.POST.get("budget")
        preferred_countries = request.POST.get("preferred_countries")


        user = User.objects.first()

        user.GPA = GPA
        user.budget = budget
        user.preferred_countries = preferred_countries

        user.save()

        return redirect("dashboard")

    return render(
        request,
        "dashboard/profile.html"
    )