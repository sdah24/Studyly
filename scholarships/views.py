from django.shortcuts import render, get_object_or_404, redirect
from .models import Scholarship
from .forms import ScholarshipForm, ScholarshipSearchForm


def scholarship_detail(request, pk):
    scholarship = get_object_or_404(
        Scholarship.objects.select_related(
            "university"
        ),
        pk=pk
    )
    return render(
        request,
        "scholarships/scholarship_detail.html",
        {
            "scholarship": scholarship
        }
    )


def scholarship_search(request):
    form = ScholarshipSearchForm(
        request.GET or None
    )
    scholarships = Scholarship.objects.select_related(
        "university"
    )
    if form.is_valid():
        query = form.cleaned_data.get("query")
        university = form.cleaned_data.get("university")
        min_amount = form.cleaned_data.get("min_amount")
        deadline_before = f