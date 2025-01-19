from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<eventId>/quiz/', views.quiz, name='quiz'),
    path('register/', views.register, name='register'),
]
