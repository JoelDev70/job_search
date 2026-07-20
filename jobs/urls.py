from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_job_board, name='accueil'), 
    path('offre/ajouter/', views.ajouter_offre, name='ajouter_offre'),
    path('offre/modifier/<int:id>/', views.modifier_offre, name='modifier_offre'),
    path('offre/supprimer/<int:id>/', views.supprimer_offre, name='supprimer_offre'),
    
]
