from django.db import models
from core.models import Institution
from datetime import date

class GeneralNotice(models.Model):
    name = models.CharField(max_length=200, verbose_name='İsim')
    notice = models.TextField(verbose_name='Announcement')
    image = models.ImageField(upload_to='announcement/', blank=True, null=True, verbose_name='Resim')
    time = models.DateField(default=date.today, verbose_name='Date')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "General Announcement"
        verbose_name_plural = "Genaral Announcements"
        ordering = ["-time"]
        get_latest_by = "time" 

class InstitutionNotice(models.Model):
    name = models.ForeignKey(GeneralNotice, on_delete=models.CASCADE, related_name="institution_notice", verbose_name="Program")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="institution_notice", verbose_name="Institution")
    instutionnotice = models.TextField(verbose_name='Program schedule, additional announcement information, announcements:')

    def get_message_as_html(self):
        return self.instutionnotice.replace('\n', '<br>')

    class Meta:
        verbose_name = "Institution Announcement"
        verbose_name_plural = "Institution Announcements"
        ordering = ["-name"]