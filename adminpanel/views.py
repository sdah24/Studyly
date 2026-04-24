from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from universities.models import University
from scholarships.models import Scholarship
from applications.models import Application


# ── Role guard ─────────────────────────────────────────────────────────────────
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'admin':
            return redirect('dashboard:dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# Every admin context gets skip_nav=True so base.html hides the student nav
def admin_ctx(extra=None):
    ctx = {'skip_nav': True}
    if extra:
        ctx.update(extra)
    return ctx


# ── Dashboard ──────────────────────────────────────────────────────────────────
@admin_required
def dashboard(request):
    context = admin_ctx({
        'total_students':     User.objects.filter(role='student').count(),
        'total_universities': University.objects.count(),
        'total_applications': Application.objects.count(),
        'total_scholarships': Scholarship.objects.count(),
        'recent_applications': Application.objects.select_related(
            'user', 'university', 'program'
        ).order_by('-applied_date')[:8],
        'active_sidebar': 'dashboard',
    })
    return render(request, 'adminpanel/dashboard.html', context)


# ── Students ───────────────────────────────────────────────────────────────────
@admin_required
def students(request):
    q = request.GET.get('q', '').strip()
    student_list = User.objects.filter(role='student').select_related('profile').order_by('-date_joined')
    if q:
        student_list = (
            student_list.filter(username__icontains=q) |
            student_list.filter(email__icontains=q) |
            student_list.filter(first_name__icontains=q) |
            student_list.filter(last_name__icontains=q)
        )
    return render(request, 'adminpanel/students.html', admin_ctx({
        'students': student_list,
        'q': q,
        'active_sidebar': 'students',
    }))


@admin_required
def promote_to_admin(request, pk):
    """Make any user an admin — POST only."""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        user.role = 'admin'
        user.save()
        messages.success(request, f'{user.username} is now an Admin.')
    return redirect('adminpanel:students')


# ── Universities ───────────────────────────────────────────────────────────────
@admin_required
def universities(request):
    return render(request, 'adminpanel/universities.html', admin_ctx({
        'universities': University.objects.all().order_by('ranking'),
        'active_sidebar': 'universities',
    }))


@admin_required
def university_create(request):
    if request.method == 'POST':
        University.objects.create(
            name=request.POST.get('name'),
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            ranking=request.POST.get('ranking') or None,
            rating=request.POST.get('rating') or None,
            tuition_display=request.POST.get('tuition_display'),
            acceptance_rate=request.POST.get('acceptance_rate') or None,
            min_gpa=request.POST.get('min_gpa') or None,
            min_ielts=request.POST.get('min_ielts') or None,
            website=request.POST.get('website'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'University added successfully.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/university_form.html', admin_ctx({
        'active_sidebar': 'universities', 'action': 'Add'
    }))


@admin_required
def university_edit(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        uni.name            = request.POST.get('name')
        uni.country         = request.POST.get('country')
        uni.city            = request.POST.get('city')
        uni.ranking         = request.POST.get('ranking') or None
        uni.rating          = request.POST.get('rating') or None
        uni.tuition_display = request.POST.get('tuition_display')
        uni.acceptance_rate = request.POST.get('acceptance_rate') or None
        uni.min_gpa         = request.POST.get('min_gpa') or None
        uni.min_ielts       = request.POST.get('min_ielts') or None
        uni.website         = request.POST.get('website')
        uni.description     = request.POST.get('description')
        uni.save()
        messages.success(request, 'University updated successfully.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/university_form.html', admin_ctx({
        'uni': uni, 'active_sidebar': 'universities', 'action': 'Edit'
    }))


@admin_required
def university_delete(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        uni.delete()
        messages.success(request, 'University deleted.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/confirm_delete.html', admin_ctx({
        'object_name': uni.name, 'active_sidebar': 'universities',
        'cancel_url': 'adminpanel:universities',
    }))


# ── Scholarships ───────────────────────────────────────────────────────────────
@admin_required
def scholarships(request):
    return render(request, 'adminpanel/scholarships.html', admin_ctx({
        'scholarships': Scholarship.objects.all().order_by('deadline'),
        'active_sidebar': 'scholarships',
    }))


@admin_required
def scholarship_create(request):
    unis = University.objects.all().order_by('name')
    if request.method == 'POST':
        Scholarship.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            provider=request.POST.get('provider'),
            university_id=request.POST.get('university') or None,
            amount=request.POST.get('amount') or None,
            amount_display=request.POST.get('amount_display'),
            funding_type=request.POST.get('funding_type', 'full'),
            category=request.POST.get('category', 'merit'),
            deadline=request.POST.get('deadline'),
            target_group=request.POST.get('target_group'),
            recipients_per_year=request.POST.get('recipients_per_year'),
            min_gpa_required=request.POST.get('min_gpa_required') or None,
            min_ielts_required=request.POST.get('min_ielts_required') or None,
        )
        messages.success(request, 'Scholarship added successfully.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/scholarship_form.html', admin_ctx({
        'universities': unis, 'active_sidebar': 'scholarships', 'action': 'Add'
    }))


@admin_required
def scholarship_edit(request, pk):
    schol = get_object_or_404(Scholarship, pk=pk)
    unis = University.objects.all().order_by('name')
    if request.method == 'POST':
        schol.title               = request.POST.get('title')
        schol.description         = request.POST.get('description')
        schol.provider            = request.POST.get('provider')
        schol.university_id       = request.POST.get('university') or None
        schol.amount              = request.POST.get('amount') or None
        schol.amount_display      = request.POST.get('amount_display')
        schol.funding_type        = request.POST.get('funding_type', 'full')
        schol.category            = request.POST.get('category', 'merit')
        schol.deadline            = request.POST.get('deadline')
        schol.target_group        = request.POST.get('target_group')
        schol.recipients_per_year = request.POST.get('recipients_per_year')
        schol.min_gpa_required    = request.POST.get('min_gpa_required') or None
        schol.min_ielts_required  = request.POST.get('min_ielts_required') or None
        schol.save()
        messages.success(request, 'Scholarship updated successfully.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/scholarship_form.html', admin_ctx({
        'schol': schol, 'universities': unis,
        'active_sidebar': 'scholarships', 'action': 'Edit'
    }))


@admin_required
def scholarship_delete(request, pk):
    schol = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        schol.delete()
        messages.success(request, 'Scholarship deleted.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/confirm_delete.html', admin_ctx({
        'object_name': schol.title, 'active_sidebar': 'scholarships',
        'cancel_url': 'adminpanel:scholarships',
    }))