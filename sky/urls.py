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
    path('topic_by_name/<str:name>/', views.topic_by_name),

    path('tree/<int:id>/', views.tree),

    path('add_item/<int:id>/<int:location>/', views.add_item),
    path('move_item/<int:id>/', views.move_item),

    path('change_item/<int:id>/', views.change_item),
    path('change_txt/<int:id>/', views.change_txt),

    path('change_figure/<int:id>/', views.change_figure),

    path('upgrade/', views.upgrade),
    path('news/', views.news),
    re_path('^', views.index, name='index'),
]
