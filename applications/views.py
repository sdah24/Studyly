from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm
from universities.models import University


@login_required
def application_list(request):
    applications = Application.objects.filter(
        user=request.user
    ).select_related('university', 'program')

    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    all_apps     = Application.objects.filter(user=request.user)
    total        = all_apps.count()
    accepted     = all_apps.filter(status='accepted').count()
    under_review = all_apps.filter(status='under_review').count()
    incomplete   = all_apps.filter(status='incomplete').count()
    rejected     = all_apps.filter(status='rejected').count()
    submitted    = all_apps.filter(status='submitted').count()

    return render(request, 'applications/applications.html', {
        'applications':  applications,
        'status_filter': status_filter,
        'total':         total,
        'accepted':      accepted,
        'under_review':  under_review,
        'incomplete':    incomplete,
        'rejected':      rejected,
        'submitted':     submitted,
    })


@login_required
def application_create(request):
    initial = {}
    uni_pk = request.GET.get('university')
    if uni_pk:
        try:
            initial['university'] = University.objects.get(pk=uni_pk)
        except University.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)  # request.FILES for uploads
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()  # auto-sets status based on uploaded docs
            messages.success(request, f'Application to {app.university.name} created!')
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ApplicationForm(initial=initial)

    return render(request, 'applications/application_form.html', {
        'form':  form,
        'title': 'New Application',
    })


@login_required
def application_detail(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'app': app})


@login_required
def application_update(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=app)  # request.FILES
        if form.is_valid():
            form.save()  # auto-sets status
            messages.success(request, 'Application updated!')
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ApplicationForm(instance=app)

    return render(request, 'applications/application_form.html', {
        'form':  form,
        'app':   app,
        'title': f'Edit — {app.university.name}',
    })


@login_required
def application_delete(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        name = app.university.name
        app.delete()
        messages.success(request, f'Application to {name} deleted.')
        return redirect('applications:list')
    return render(request, 'applications/application_confirm_delete.html', {'app': app})