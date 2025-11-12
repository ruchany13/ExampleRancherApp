from django.shortcuts import render
from datetime import date, timedelta

from core.models import Student, Institution
from announcement.models import InstitutionNotice, GeneralNotice
from .models import LevelReport, GradeReport, Tracking
from . import forms

# Create your views here.
def search_student(request):
    form = forms.StudentSearch(request.GET or None)
    today = date.today()

    # If today is not Saturday or Sunday, it sends the following message to the search page and no search is performed.
    if today.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
        pass
    else:
        return render(request, "search.html", {"form": form, "error_message": "Dear Parent! The weekly activity records have not been added yet. Please try again on Saturday or Sunday."})
    
    
    if form.is_valid():
        name = form.cleaned_data["name"]
        surname = form.cleaned_data["surname"]
        context = {}

        try:
            
            context["student"] = Student.objects.select_related("institution").get(
                first_name__iexact=name,
                last_name__iexact=surname
            )
            
            # It is necessary to show one of the multiple selections by adding a date here
            # It retrieves the data for that class by using the class information from the student's details
            context["grade"] = GradeReport.objects.filter(
                grade__iexact=context["student"].grade,  # students["grade"] ❌ → students.grade ✅
                institution__exact=context["student"].institution
            ).latest('time')


            context["level"] = LevelReport.objects.filter(
                level__iexact=context["student"].level, 
                institution__exact=context["student"].institution
                #time='2025-09-12'
            ).latest('time')


            # ----------------- If there are less than 10 days to the bulk message date, show the messages -----------------
            today = date.today()
            ten_days_later = today + timedelta(days=10)
            general_notices = GeneralNotice.objects.filter(
                time__gte=today,
                time__lte=ten_days_later
            )

            if general_notices.exists():
                context["generalNotice"] = general_notices
                context["institutionNotice"] = InstitutionNotice.objects.filter(
                    institution=context["student"].institution,
                    name__in=general_notices
                )



            # --------------- When a student name is searched, save the week/year for dashboards -----------------
            iso = date.today().isocalendar()

            student_for_tracking = Tracking.objects.filter(
                student=context["student"],
                iso_week=iso.week,
                iso_year=iso.year
            ).exists()

            # If a record exists for the student in this week/year, pass; otherwise, add a new record
            if student_for_tracking:
                pass
            else:
                Tracking.objects.create(student=context["student"])

            # student found $\to$ show results on a separate page
            return render(request, "student_result.html",context)

        except Student.DoesNotExist:
            return render(request, "search.html", {"form": form, "error_message": "Sorry, the student you are looking for could not be found. Please check the spelling of the first and last name and try again."})
        except (LevelReport.DoesNotExist , GradeReport.DoesNotExist):
            return render(request, "search.html", {"form": form, "error_message": "Sorry, no weekly activity entries were found for the student you are looking for."})
        except Student.MultipleObjectsReturned:
            return render(request, "search.html", {"form": form, "error_message": "There is a user with the same name!"})

    return render(request, "search.html", {"form": form})
