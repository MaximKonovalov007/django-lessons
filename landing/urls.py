from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    #path('/landing/', views.landing, name='landing'),
    re_path('^$', views.home, name='home'),
]
