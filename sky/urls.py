from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('ajax/<int:node>/<int:you>/', views.ajax),
    re_path('^interest_search/', views.interest_search, name='interest_search'),
    re_path('^topic_search/', views.topic_search, name='topic_search'),
    re_path('^topic_tree/(\d+)/', views.topic_tree, name='topic_tree'),
    re_path('^news/', views.news, name='news'),
    re_path('^', views.index, name='index'),
]
