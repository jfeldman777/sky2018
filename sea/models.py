from django.db import models
from sky.models import MagicNode

class Boat(models.Model):
    node = models.ForeignKey(MagicNode,on_delete=models.CASCADE)
    link = models.URLField(null=True, blank=True)
    name = models.CharField(null=False,blank=False, max_length=100)
    desc = models.TextField(null=False,blank=False)
    n_sib = models.PositiveIntegerField()
    class Meta:
        ordering = ['n_sib',]

    def __str__(self):
        return self.name
