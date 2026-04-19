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

    from django.shortcuts import render, redirect

    from .forms import ScholarshipForm

    def add_scholarship(request):

        if request.method == "POST":

            form = ScholarshipForm(

                request.POST

            )

            if form.is_valid():
                form.save()

                return redirect(
                    "scholarships:list"
                )

        else:

            form = ScholarshipForm()

        return render(

            request,

            "scholarships/add_scholarship.html",

            {

                "form": form

            }

        )