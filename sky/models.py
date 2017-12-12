from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
# Create your models here.
class NewsRecord(models.Model):

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=_("Content"),
        blank=False)

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name=_("Figure"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated_at','-created_at',]
