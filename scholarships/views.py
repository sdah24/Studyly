from .models import Scholarship
from .forms import ScholarshipSearchForm


def scholarship_search(request):

    form = ScholarshipSearchForm(

        request.GET or None

    )

    scholarships = Scholarship.objects.select_related(
        "university"
    )

    if form.is_valid():

        query = form.cleaned_data.get(
            "query"
        )

        if query:

            scholarships = scholarships.filter(

                title__icontains=query

            )

    context = {

        "form": form,

        "scholarships": scholarships,

    }

    return render(

        request,

        "scholarships/scholarship_search.html",

        context

    )