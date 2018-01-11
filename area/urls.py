from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('report2/<int:id>/', views.report2),
    path('bag/<int:id>/', views.bag),

    path('create', views.area_create),
    path('admin/', views.areas_admin),
    path('using/', views.using_areas),
]
