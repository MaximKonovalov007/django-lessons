from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('product/<product_id>', views.product, name='product'),
]
