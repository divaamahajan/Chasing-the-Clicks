"""
URL configuration for chasing_the_clicks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from clicks_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('savejson', views.save_location_count, name='save_location_count'),
    path('stats.html', views.get_stats, name='get_stats'),
    path('get_stats', views.get_stats, name='get_stats'),
    # path('', views.home, name='home'),
    path('clickCounter.html', views.clickCounter, name='clickCounter'),
    path('/', views.clickCounter, name='clickCounter'),
    path('', views.clickCounter, name='clickCounter'),
    # path('index.html/', views.home, name='home'),
    # path('get-data/', views.get_data, name='get-data'),
]
urlpatterns += staticfiles_urlpatterns()