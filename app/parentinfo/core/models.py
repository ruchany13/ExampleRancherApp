from django.db import models
from django.conf import settings

GENDER = [
    ("male","male"),
    ("female", "female"),
]

GRADES = [
    ("5", "5. Grade"),
    ("6", "6. Grade"),
    ("7", "7. Grade"),
    ("8", "8. Grade"),
]

LEVELS = [
    ("1", "Level 1"),
    ("2", "Level 2"),
    ("3", "Level 3"),
]

class Institution(models.Model):
    name = models.CharField(verbose_name='Institution Name', max_length=200)
    address = models.CharField(verbose_name='Institution Address', max_length=200)
    location = models.CharField(max_length=255, verbose_name='Location (Google Maps link or address)', blank=True, null=True)

    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name='Institution Admin',
        on_delete=models.PROTECT,
        related_name="managed_institution",
        blank=True,
        null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"
        ordering = ["name"]
        get_latest_by = "name" 


class Student(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="students", verbose_name="Institution")
    first_name = models.CharField(max_length=80,verbose_name="Student First Name")
    last_name = models.CharField(max_length=80, verbose_name="Student Last Name")
    grade = models.CharField(choices=GRADES, max_length=200, verbose_name="Student Academic Grade")
    level = models.CharField(choices=LEVELS, max_length=200, verbose_name="Student Social Level")
    status = models.BooleanField(default=True, verbose_name="Is student active ?")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["first_name"]       # liste sırası
        get_latest_by = "first_name" 