from django.shortcuts import render, get_object_or_404
from .models import Scholarship

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
    query = request.GET.get("query", "")
    scholarships = Scholarship.objects.select_related(
        "university"
    ).filter(
        title__icontains=query
    ) if query else Scholarship.objects.none()
    return render(
        r