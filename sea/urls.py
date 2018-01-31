from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('more/<int:id>/', views.more),
    path('add/<int:id>/', views.add),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),        
]
