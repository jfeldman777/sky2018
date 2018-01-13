from django.contrib import admin

from django.contrib import admin
from .models import Area, AreaPlus

# Register your models here.
class AreaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Area, AreaAdmin)

class AreaPlusAdmin(admin.ModelAdmin):
    list_display = ('node', 'area','alone','minus' )
    pass

admin.site.register(AreaPlus, AreaPlusAdmin)
