# views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from core.models import Student, Institution
from activity.models import LevelReport, GradeReport, Tracking


@staff_member_required
def main_old(request):
    data_points_institution_number = []
    institutions = Institution.objects.all()
    for inst in institutions:
        student_count = Student.objects.filter(institution=inst).count()
        data_points.append({"label": inst.name, "y": student_count})
    return render(request, "admin/dashboard.html", {"data_points": data_points})

from django.db.models import Count

def _choices_map(model, field_name):
    field = model._meta.get_field(field_name)
    return dict(field.choices)


@staff_member_required
def main(request):
    inst_qs = (
        Institution.objects
        .annotate(student_count=Count("students"))
        .values("name", "student_count")
        .order_by("name")
    )
    data_points_institution = [
        {"label": r["name"], "y": r["student_count"]}
        for r in inst_qs
    ]

    grade_labels = _choices_map(Student, "grade")  # {'5': '5. Sınıf', ...}
    grade_qs = (
        Student.objects
        .values("grade")
        .annotate(count=Count("id"))
        .order_by("grade")
    )
    data_points_grade = [
        {"label": grade_labels.get(r["grade"], str(r["grade"])), "y": r["count"]}
        for r in grade_qs
    ]

    level_labels = _choices_map(Student, "level")  # {'1': 'Seviye 1', ...}
    level_qs = (
        Student.objects
        .values("level")
        .annotate(count=Count("id"))
        .order_by("level")
    )
    data_points_level = [
        {"label": level_labels.get(r["level"], str(r["level"])), "y": r["count"]}
        for r in level_qs
    ]

    status_qs = (
        Student.objects
        .values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
    data_points_status = [
        {"label": ("Aktif" if r["status"] else "Pasif"), "y": r["count"]}
        for r in status_qs
    ]

    gender_labels = _choices_map(Institution, "gender")
    gender_qs = (
        Institution.objects
        .values("gender")
        .annotate(count=Count("id"))
        .order_by("gender")
    )
    
    data_points_institution_gender = [
        {"label": gender_labels.get(r["gender"], str(r["gender"])), "y": r["count"]}
        for r in gender_qs
    ]
    

    context = {
        "data_points_institution": data_points_institution,         # Bar chart
        "data_points_grade": data_points_grade,                     # Pie/Donut
        "data_points_level": data_points_level,                     # Pie/Donut
        "data_points_status": data_points_status,                   # Doughnut
        "data_points_institution_gender": data_points_institution_gender,  # Bar/Pie
    }

    return render(request, "admin/dashboard.html", context)