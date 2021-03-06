from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from treebeard.al_tree import AL_Node
from sky.models import MagicNode

from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Area(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    is_published = models.BooleanField(default = False)
    root = models.ForeignKey(MagicNode,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AreaPlus(models.Model):
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    node = models.ForeignKey(MagicNode,on_delete=models.CASCADE)
    alone = models.BooleanField(default = False)
    minus = models.BooleanField(default = False)

    def __str__(self):
        return self.node.desc

class Subscription(models.Model):
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'myuser')

    def __str__(self):
        a = Area.objects.get(id=self.area_id)
        return a.name
