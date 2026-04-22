from django.shortcuts import render, redirect
from users.models import User

def dashboard(request):

    return render(
        request,
        "dashboard/dashboard.html"
    )

