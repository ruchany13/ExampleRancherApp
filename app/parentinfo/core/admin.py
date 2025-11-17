from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Institution, Student


class InstitutionScopedAdminMixin:
    """
    Restricts non-superusers to the Institution they manage.
    The field for the managed institution in your User model: user.managed_institution
    The FK field in the model: institution
    """
    institution_fk_name = "institution"          
    user_institution_attr = "managed_institution"  

    def _user_institution(self, request):
        if request.user.is_superuser:
            return None
        return getattr(request.user, self.user_institution_attr, None)

    def _in_scope(self, request, obj=None):
        if request.user.is_superuser:
            return True
        inst = self._user_institution(request)
        if not inst:
            return False
        if obj is None:
            return True
        obj_inst = getattr(obj, self.institution_fk_name, None)
        return getattr(obj_inst, "id", None) == getattr(inst, "id", None)

    # --- Limit the list ---
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        inst = self._user_institution(request)
        if not inst:
            return qs.none()
        return qs.filter(**{self.institution_fk_name: inst})

    # --- permissions (global + scope) ---
    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj) and self._in_scope(request, obj)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._in_scope(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._in_scope(request, obj)

    def has_add_permission(self, request):
        return super().has_add_permission(request) and self._in_scope(request, obj=None)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == self.institution_fk_name and not request.user.is_superuser:
            inst = self._user_institution(request)
            kwargs["queryset"] = (
                Institution.objects.filter(id=inst.id) if inst else Institution.objects.none()
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            inst = self._user_institution(request)
            if not inst:
                raise ValidationError("Yönettiğiniz bir kurum (Institution) bulunamadı.")
            setattr(obj, self.institution_fk_name, inst)
        return super().save_model(request, obj, form, change)


    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and self.institution_fk_name not in ro:
            ro.append(self.institution_fk_name)
        return ro


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "manager")
    search_fields = ("name", "address", "manager__username")
    list_filter = ("name",)


@admin.register(Student)
class StudentAdmin(InstitutionScopedAdminMixin, admin.ModelAdmin):
    list_display = ("first_name", "last_name", "level", "grade", "institution", "status")
    list_filter = ("grade", "level", "status")
    search_fields = ("first_name", "last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.GET.get('status__exact'):
            qs = qs.filter(status=True)
        return qs

