from django.contrib import admin
from .models import NewsRecord

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at','updated_at' )
    fields = ('title', 'description', 'figure')

admin.site.register(NewsRecord, NewsAdmin)

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import MagicNode

class MagicAdmin(TreeAdmin):
    form = movenodeform_factory(MagicNode)

admin.site.register(MagicNode, MagicAdmin)
