from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from treebeard.al_tree import AL_Node

from django.contrib.postgres.fields import ArrayField
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
    friends = models.ManyToManyField('self',
                               blank=True,
                               )

    desc = models.CharField(max_length=255)
    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name=_("Figure"))
    text = models.TextField(
            verbose_name=_("Text"),
            blank=True)

    video = models.FileField(upload_to='uploads/%Y/%m/%d',blank=True,
                    null=True)

    sites = ArrayField(
            models.TextField(blank=True),
            blank = True,
            null=True,
            size=5,

        )

    videos = ArrayField(
                models.TextField(blank=True),
                blank = True,
                null=True,
                size=5,

            )

    pre_nodes = ArrayField(
                models.TextField(blank=True),
                blank = True,
                null=True,
                size=5,

            )

    def __str__(self):
        return self.desc

class Interest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.ForeignKey(MagicNode,on_delete=models.CASCADE)
    i_like_the_topic = models.BooleanField()
    i_like_the_content = models.BooleanField()
    i_am_an_expert = models.BooleanField()
