from django.shortcuts import get_object_or_404


def university_detail(request, pk):

    university = get_object_or_404(

        University,

        pk=pk

    )

    return render(

        request,

        "universities/university_detail.html",

        {

            "university": university

        }

    )