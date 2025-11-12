from django.db import models
from datetime import date
from core.models import Institution, Student

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

class GradeReport(models.Model):
    grade = models.CharField(choices=GRADES, max_length=200, verbose_name="Grade")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="grades")
    description = models.TextField(verbose_name="Academic activity description")
    time = models.DateField(verbose_name="Date", default=date.today)

    def __str__(self):
        return self.grade
   
    class Meta:
        verbose_name = "Academic Activity"
        verbose_name_plural = "Academic Activities"
        ordering = ["-time", "grade"]
        get_latest_by = "time" 
    
class LevelReport(models.Model):
    level = models.CharField(choices=LEVELS, max_length=200, verbose_name="Level")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="levels")
    description = models.TextField(verbose_name="Social Activity")
    time = models.DateField(verbose_name="Date", default=date.today)
    image = models.ImageField(upload_to='levels/', blank=True, null=True, verbose_name='Image')

    class Meta:
        verbose_name = "Social Activity"
        verbose_name_plural = "Social Activities"
        ordering = ["-time", "level"] 
        get_latest_by = "time"

    def __str__(self):
        return f"{self.level} {self.time}"

class Tracking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="trackings", verbose_name="Student")
    iso_year = models.PositiveIntegerField(default=date.today().isocalendar()[0])
    iso_week = models.PositiveIntegerField(default=date.today().isocalendar()[1])

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} {self.iso_week}"