from django.contrib import admin

from django.contrib import admin
from .models import Area, AreaPlus, Subscription

# Register your models here.
class AreaAdmin(admin.ModelAdmin):
    list_display = ('user', 'name','root' )    
    pass

admin.site.register(Area, AreaAdmin)

class AreaPlusAdmin(admin.ModelAdmin):
    list_display = ('node', 'area','alone','minus' )
    pass

admin.site.register(AreaPlus, AreaPlusAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'area')
    pass

admin.site.register(Subscription, SubscriptionAdmin)
