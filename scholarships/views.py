from django.shortcuts import render, get_object_or_404
from .models import Scholarship
from .models import Scholarship
from .forms import ScholarshipForm

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

    from django.shortcuts import get_object_or_404

    def edit_scholarship(request, pk):

        scholarship = get_object_or_404(

            Scholarship,

            pk=pk

        )

        if request.method == "POST":

            form = ScholarshipForm(

                request.POST,

                instance=scholarship

            )

            if form.is_valid():
                form.save()

                return redirect(
                    "scholarships:list"
                )

        else:

            form = ScholarshipForm(

                instance=scholarship

            )

        return render(

            request,

            "scholarships/edit_scholarship.html",

            {

                "form": form,

                "scholarship": scholarship

            }

        )

    from django.shortcuts import get_object_or_404, redirect, render

    from .models import Scholarship

    def delete_scholarship(request, pk):

        scholarship = get_object_or_404(
            Scholarship,
            pk=pk
        )

        if request.method == "POST":
            scholarship.delete()

            return redirect(
                "scholarships:list"
            )

        return render(

            request,

            "scholarships/delete_scholarship.html",

            {
                "scholarship": scholarship
            }

        )