from django.contrib import admin
from .models import GeneralNotice, InstitutionNotice
from core.admin import InstitutionScopedAdminMixin


@admin.register(GeneralNotice)
class GeneralNoticeAdmin(admin.ModelAdmin):
    list_display = ("name", "time", "notice")
    search_fields = ("name", "notice")
    list_filter = ("time",)


@admin.register(InstitutionNotice)
class InstitutionNoticeAdmin(InstitutionScopedAdminMixin, admin.ModelAdmin):
    list_display = ("name", "instutionnotice")
    search_fields = ("name", "instutionnotice")
