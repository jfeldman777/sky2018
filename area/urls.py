from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('report3/<int:sub_id>/<int:node_id>/', views.report3),

    path('col1/<int:id>/<int:line_id>/', views.col1),
    path('col2/<int:id>/<int:line_id>/', views.col2),

    path('report2/<int:id>/', views.report2),
    path('bag/<int:id>/', views.bag),

    path('pub/<int:id>/', views.pub),
    path('unpub/<int:id>/', views.unpub),

    path('sub/<int:id>/', views.sub),
    path('unsub/<int:id>/', views.unsub),

    path('rename/<int:id>/', views.rename),

    path('add/<int:area_id>/', views.add),
    path('delete/<int:id>/', views.delete_area),
    path('delete_line/<int:id>/<int:line_id>/', views.delete_line),

    path('create/', views.area_create),
    path('admin/', views.areas_admin),
    path('using/', views.using_areas),
]
