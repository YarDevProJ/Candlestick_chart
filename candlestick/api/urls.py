# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('candles/', views.get_candles, name='get_candles'),
]