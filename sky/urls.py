from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^news/', views.news, name='news'),
    re_path('^', views.index, name='index'),    
]
