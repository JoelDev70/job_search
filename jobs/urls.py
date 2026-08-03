from django.urls import path
from . import views

urlpatterns = [
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('', views.accueil_job_board, name='accueil'), 
    path('list_jobs/', views.lister_offres, name='liste_offres'), 
    path('companies/', views.profile_entreprise, name='profile_entreprise'),
    path('recruteur/tableau-de-bord/', views.dashboard_recruteur, name='dashboard_recruteur'),
    path('recruteur/profil/', views.profile_recruteur, name='profile_recruteur'),
    path('offre/<int:id>/', views.detail_offre, name='detail_offre'),
    path('offre/<int:id>/postuler/', views.postuler_offre, name='postuler_offre'),
    path('candidature/<int:id>/statut/', views.modifier_statut_candidature, name='modifier_statut_candidature'),
    path('offre/<int:id>/rapport-candidatures/', views.rapport_candidatures, name='rapport_candidatures'),
    
    path('offre/ajouter/', views.ajouter_offre, name='ajouter_offre'),
    path('offre/modifier/<int:id>/', views.modifier_offre, name='modifier_offre'),
    path('offre/supprimer/<int:id>/', views.supprimer_offre, name='supprimer_offre'),
    
]
