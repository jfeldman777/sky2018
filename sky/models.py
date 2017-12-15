from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from treebeard.al_tree import AL_Node
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

class MagicNode(AL_Node):
    parent = models.ForeignKey('self',
                               related_name='children_set',
                               null=True,
                               db_index=True,on_delete=models.CASCADE)
    sib_order = models.PositiveIntegerField()
    desc = models.CharField(max_length=255)

    text = models.TextField(
            verbose_name=_("Text"),
            blank=True)

    video = models.FileField(upload_to='uploads/%Y/%m/%d',blank=True,
                    null=True)
    def __str__(self):
        return self.desc
