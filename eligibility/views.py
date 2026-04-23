from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from universities.models import University
from scholarships.models import Scholarship
from datetime import date


def _score_label(score):
    if score >= 85:
        return "Strong Candidate"
    elif score >= 70:
        return "Good Candidate"
    elif score >= 50:
        return "Moderate Candidate"
    else:
        return "Needs Improvement"


def _compute_scholarship_match(scholarship, profile):
    """
    Returns an integer 0–100 representing how well the student matches
    a given scholarship, based on GPA and IELTS requirements.
    """
    factors = []

    # GPA factor
    if scholarship.min_gpa_required and profile.GPA is not None:
        if profile.GPA >= scholarship.min_gpa_required:
            # How far above the threshold?
            surplus = profile.GPA - scholarship.min_gpa_required
            factors.append(min(100, int(70 + surplus * 30)))
        else:
            deficit = scholarship.min_gpa_required - profile.GPA
            factors.append(max(0, int(50 - deficit * 25)))
    elif profile.GPA is not None:
        factors.append(75)  # no GPA requirement — base score

    # IELTS factor
    if scholarship.min_ielts_required and profile.english_score is not None:
        if profile.english_score >= scholarship.min_ielts_required:
            surplus = profile.english_score - scholarship.min_ielts_required
            factors.append(min(100, int(70 + surplus * 15)))
        else:
            deficit = scholarship.min_ielts_required - profile.english_score
            factors.append(max(0, int(50 - deficit * 20)))
    elif profile.english_score is not None:
        factors.append(75)

    if not factors:
        return 70  # default when no requirements set

    return int(sum(factors) / len(factors))


@login_required
def check(request):
    profile = request.user.profile

    criteria = []
    score_points = 0
    recommendations = []

    # ── 1. GPA / Academic ─────────────────────────────────────────────────────
    gpa = profile.GPA
    degree = profile.get_degree_level_display() if profile.degree_level else None

    if gpa is not None:
        if gpa >= 3.5:
            criteria.append({
                'icon': 'check-circle',
                'icon_color': '#16a34a',
                'title': 'Academic Qualifications',
                'detail': f"{degree or 'Degree'} with {gpa:.2f} GPA",
                'badge': 'Passed',
                'badge_bg': '#dcfce7',
                'badge_color': '#15803d',
            })
            score_points += 25
        elif gpa >= 2.8:
            criteria.append({
                'icon': 'alert-circle',
                'icon_color': '#ca8a04',
                'title': 'Academic Qualifications',
                'detail': f"{degree or 'Degree'} with {gpa:.2f} GPA (3.5+ preferred)',",
                'badge': 'Needs Improvement',
                'badge_bg': '#fffbeb',
                'badge_color': '#a16207',
            })
            score_points += 15
            recommendations.append("Aim for a GPA of 3.5 or higher to unlock more university options.")
        else:
            criteria.append({
                'icon': 'x-circle',
                'icon_color': '#dc2626',
                'title': 'Academic Qualifications',
                'detail': f"{degree or 'Degree'} with {gpa:.2f} GPA — below most thresholds",
                'badge': 'Action Required',
                'badge_bg': '#fef2f2',
                'badge_color': '#b91c1c',
            })
            recommendations.append("Your GPA is below the minimum for most universities. Seek academic improvement or alternative entry paths.")
    else:
        criteria.append({
            'icon': 'x-circle',
            'icon_color': '#dc2626',
            'title': 'Academic Qualifications',
            'detail': 'GPA not set — update your profile',
            'badge': 'Action Required',
            'badge_bg': '#fef2f2',
            'badge_color': '#b91c1c',
        })
        recommendations.append("Add your GPA to your profile so we can accurately assess your eligibility.")

    # ── 2. English Proficiency ────────────────────────────────────────────────
    lang = profile.english_proficiency
    score = profile.english_score

    if lang and lang != 'none' and score is not None:
        test_name = profile.get_english_proficiency_display()
        threshold = 6.5 if lang == 'ielts' else 80  # IELTS vs TOEFL

        if score >= threshold + (1.0 if lang == 'ielts' else 10):
            criteria.append({
                'icon': 'check-circle',
                'icon_color': '#16a34a',
                'title': 'English Proficiency',
                'detail': f"{test_name} {score}",
                'badge': 'Passed',
                'badge_bg': '#dcfce7',
                'badge_color': '#15803d',
            })
            score_points += 20
        elif score >= threshold:
            criteria.append({
                'icon': 'check-circle',
                'icon_color': '#16a34a',
                'title': 'English Proficiency',
                'detail': f"{test_name} {score} (meets minimum)',",
                'badge': 'Passed',
                'badge_bg': '#dcfce7',
                'badge_color': '#15803d',
            })
            score_points += 14
        else:
            criteria.append({
                'icon': 'alert-circle',
                'icon_color': '#ca8a04',
                'title': 'English Proficiency',
                'detail': f"{test_name} {score} — below the {threshold} minimum",
                'badge': 'Needs Improvement',
                'badge_bg': '#fffbeb',
                'badge_color': '#a16207',
            })
            score_points += 5
            recommendations.append(
                f"Improve your {test_name} score to at least {threshold} to meet most university requirements."
            )
    else:
        criteria.append({
            'icon': 'x-circle',
            'icon_color': '#dc2626',
            'title': 'English Proficiency',
            'detail': 'No English test score on record',
            'badge': 'Action Required',
            'badge_bg': '#fef2f2',
            'badge_color': '#b91c1c',
        })
        recommendations.append("Take IELTS or TOEFL and add your score to your profile.")

    # ── 3. Work Experience ────────────────────────────────────────────────────
    exp = profile.work_experience_years or 0
    if exp >= 3:
        criteria.append({
            'icon': 'check-circle',
            'icon_color': '#16a34a',
            'title': 'Work Experience',
            'detail': f"{exp} years of professional experience",
            'badge': 'Passed',
            'badge_bg': '#dcfce7',
            'badge_color': '#15803d',
        })
        score_points += 20
    elif exp >= 1:
        criteria.append({
            'icon': 'alert-circle',
            'icon_color': '#ca8a04',
            'title': 'Work Experience',
            'detail': f"{exp} year{'s' if exp != 1 else ''} (3+ recommended for scholarships)",
            'badge': 'Needs Improvement',
            'badge_bg': '#fffbeb',
            'badge_color': '#a16207',
        })
        score_points += 10
        recommendations.append("Consider gaining more work experience — 3+ years significantly boosts scholarship eligibility.")
    else:
        criteria.append({
            'icon': 'alert-circle',
            'icon_color': '#ca8a04',
            'title': 'Work Experience',
            'detail': "No work experience listed",
            'badge': 'Needs Improvement',
            'badge_bg': '#fffbeb',
            'badge_color': '#a16207',
        })
        recommendations.append("Add any work, volunteer, or internship experience to strengthen your profile.")

    # ── 4. Preferred Countries / Destination ─────────────────────────────────
    countries = profile.preferred_countries_list()
    if countries:
        criteria.append({
            'icon': 'check-circle',
            'icon_color': '#16a34a',
            'title': 'Study Destination',
            'detail': f"Preferences set: {', '.join(countries[:3])}{'…' if len(countries) > 3 else ''}",
            'badge': 'Passed',
            'badge_bg': '#dcfce7',
            'badge_color': '#15803d',
        })
        score_points += 10
    else:
        criteria.append({
            'icon': 'alert-circle',
            'icon_color': '#ca8a04',
            'title': 'Study Destination',
            'detail': 'No preferred countries selected',
            'badge': 'Needs Improvement',
            'badge_bg': '#fffbeb',
            'badge_color': '#a16207',
        })
        recommendations.append("Add preferred study destinations to your profile so we can tailor university matches.")

    # ── 5. Budget ─────────────────────────────────────────────────────────────
    if profile.budget and profile.budget > 0:
        criteria.append({
            'icon': 'check-circle',
            'icon_color': '#16a34a',
            'title': 'Financial Planning',
            'detail': f"Budget set: ${profile.budget:,.0f}",
            'badge': 'Passed',
            'badge_bg': '#dcfce7',
            'badge_color': '#15803d',
        })
        score_points += 10
    else:
        criteria.append({
            'icon': 'x-circle',
            'icon_color': '#dc2626',
            'title': 'Financial Planning',
            'detail': 'No budget specified — financial docs may be required',
            'badge': 'Action Required',
            'badge_bg': '#fef2f2',
            'badge_color': '#b91c1c',
        })
        recommendations.append("Set a study budget on your profile to help assess financial eligibility requirements.")

    # ── 6. Profile Completeness ───────────────────────────────────────────────
    filled = sum([
        bool(profile.GPA),
        bool(profile.degree_level),
        bool(profile.english_score),
        bool(profile.preferred_countries),
        bool(profile.budget),
        bool(profile.phone_number),
        bool(profile.date_of_birth),
    ])
    completeness = int((filled / 7) * 100)

    if completeness >= 85:
        criteria.append({
            'icon': 'check-circle',
            'icon_color': '#16a34a',
            'title': 'Profile Completeness',
            'detail': f"{completeness}% complete",
            'badge': 'Passed',
            'badge_bg': '#dcfce7',
            'badge_color': '#15803d',
        })
        score_points += 15
    elif completeness >= 50:
        criteria.append({
            'icon': 'alert-circle',
            'icon_color': '#ca8a04',
            'title': 'Profile Completeness',
            'detail': f"{completeness}% complete — fill in remaining fields",
            'badge': 'Needs Improvement',
            'badge_bg': '#fffbeb',
            'badge_color': '#a16207',
        })
        score_points += 7
        recommendations.append("Complete your profile to unlock more accurate matching results.")
    else:
        criteria.append({
            'icon': 'x-circle',
            'icon_color': '#dc2626',
            'title': 'Profile Completeness',
            'detail': f"Only {completeness}% complete",
            'badge': 'Action Required',
            'badge_bg': '#fef2f2',
            'badge_color': '#b91c1c',
        })
        recommendations.append("Your profile is incomplete. Please fill in your academic details, English scores, and preferences.")

    # ── Clamp total score ─────────────────────────────────────────────────────
    total_score = min(100, score_points)

    # ── Matched Universities ───────────────────────────────────────────────────
    all_universities = University.objects.all()
    matched_universities = []
    for uni in all_universities:
        gpa_ok = (uni.min_gpa is None) or (gpa is not None and gpa >= uni.min_gpa)
        ielts_ok = (uni.min_ielts is None) or (score is not None and score >= uni.min_ielts)
        if gpa_ok and ielts_ok:
            matched_universities.append(uni)

    # ── Matched Scholarships with % ───────────────────────────────────────────
    today = date.today()
    all_scholarships = Scholarship.objects.filter(deadline__gte=today)
    scholarship_matches = []
    for s in all_scholarships:
        match_pct = _compute_scholarship_match(s, profile)
        if match_pct >= 50:
            scholarship_matches.append({
                'scholarship': s,
                'match_pct': match_pct,
            })
    # Sort by match % descending, take top 3 for the card
    scholarship_matches.sort(key=lambda x: x['match_pct'], reverse=True)
    top_scholarships = scholarship_matches[:3]

    # ── Static recommendations if none generated ──────────────────────────────
    if not recommendations:
        recommendations.append("Prepare strong recommendation letters from academic supervisors.")
        recommendations.append("Update your CV to highlight research and leadership experience.")

    recommendations.append("Research each university's specific requirements before applying.")

    context = {
        'score': total_score,
        'score_label': _score_label(total_score),
        'criteria': criteria,
        'matched_universities_count': len(matched_universities),
        'scholarship_matches_count': len(scholarship_matches),
        'top_scholarships': top_scholarships,
        'recommendations': recommendations,
        'profile': profile,
        'active_nav': 'eligibility',
    }
    return render(request, 'eligibility/check.html', context)