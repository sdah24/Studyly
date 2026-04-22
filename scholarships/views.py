from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Scholarship
from .forms import ScholarshipSearchForm


# Scholarships main page with filters
def scholarships_view(request):

    form = ScholarshipSearchForm(
        request.GET or None
    )

    scholarships = Scholarship.objects.select_related(
        "university"
    ).all()

    if form.is_valid():

        query = form.cleaned_data.get("query")
        university = form.cleaned_data.get("university")
        category = form.cleaned_data.get("category")
        min_amount = form.cleaned_data.get("min_amount")
        deadline_before = form.cleaned_data.get("deadline_before")

        # Search title
        if query:
            scholarships = scholarships.filter(
                title__icontains=query
            )

        # Filter university
        if university:
            scholarships = scholarships.filter(
                university=university
            )

        # Filter category
        if category:
            scholarships = scholarships.filter(
                category__icontains=category
            )

        # Filter amount
        if min_amount:
            scholarships = scholarships.filter(
                amount__gte=min_amount
            )

        # Filter deadline
        if deadline_before:
            scholarships = scholarships.filter(
                deadline__lte=deadline_before
            )

    # Pagination (important for UI grid)
    paginator = Paginator(
        scholarships,
        9
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        "form": form,
        "scholarships": page_obj,
        "page_obj": page_obj,

    }

    return render(

        request,
        "scholarships/scholarships.html",
        context

    )


# Scholarship detail page
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

from django.shortcuts import redirect
from .forms import ScholarshipForm


def add_scholarship(request):

    if request.method == "POST":

        form = ScholarshipForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("scholarships:list")

    else:

        form = ScholarshipForm()

    return render(

        request,
        "scholarships/add_scholarship.html",

        {
            "form": form
        }

    )


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
                "scholarships:detail",
                pk=pk
            )

    else:

        form = ScholarshipForm(
            instance=scholarship
        )

    return render(

        request,
        "scholarships/edit_scholarship.html",

        {
            "form": form
        }

    )


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