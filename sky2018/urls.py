"""sky2018 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import include
from machina.app import board

from sky import views as core_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []

if settings.DEBUG:#в этом режиме медиафайлы берутся из статической папки MEDIA
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
]

urlpatterns += [

    re_path('^newsletter/', include('newsletter.urls')),

    path('sea/', include('sea.urls')),
    path('area/', include('area.urls')),

    re_path('^signup/$', core_views.signup, name='signup'),
    re_path('^password_change/done/$', core_views.password_change_done,
        name='password_change_done'),
    re_path('^reset/done/$', core_views.password_reset_done, name='password_reset_done'),

    re_path('^forum/', include(board.urls)),

    re_path('^', include('django.contrib.auth.urls')),
    re_path('^', include('sky.urls')),
]
