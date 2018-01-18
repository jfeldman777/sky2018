from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('ajax/<int:node>/<int:you>/', views.ajax),
    path('interest_search/', views.interest_search),
    path('expert_search/', views.expert_search),
    path('topic_search/', views.topic_search),

    path('report/<int:id>/', views.report),
    path('topic_tree/<int:id>/', views.topic_tree),

    path('upgrade/', views.upgrade),
    path('news/', views.news),
    re_path('^', views.index, name='index'),
]
