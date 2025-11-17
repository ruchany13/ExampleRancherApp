from django.contrib import admin
from core.admin import InstitutionScopedAdminMixin
from .models import GradeReport, LevelReport , Tracking

@admin.register(GradeReport)
class GradeReportAdmin(InstitutionScopedAdminMixin, admin.ModelAdmin):
    list_display = ("grade", "time","description")
    #list_display_links = ("id",)
    list_filter = ("grade", "time")
    search_fields = ( "grade","id","institution")
    date_hierarchy = "time"
    ordering = ("-time",)
    list_per_page = 50 

@admin.register(LevelReport)
class LevelReportAdmin(InstitutionScopedAdminMixin, admin.ModelAdmin):
    list_display = ("level", "institution", "time","description")
    list_filter = ("level","institution")
    search_fields = ("description",)
