from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_job_board, name='accueil'), 
]
