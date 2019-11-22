from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from defense_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = "defense_app"

urlpatterns = [
    path('', views.home, name='home'),
]
urlpatterns += staticfiles_urlpatterns()
