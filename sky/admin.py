from django.contrib import admin
from .models import NewsRecord

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at','updated_at' )
    fields = ('title', 'description', 'figure')

admin.site.register(NewsRecord, NewsAdmin)
