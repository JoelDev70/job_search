from django.shortcuts import render
from .models import Jobs  # Importe votre modèle extrait de XAMPP

def accueil_job_board(request):
    # 1. On récupère toutes les offres d'emploi enregistrées dans XAMPP
    # .select_related() permet de charger l'entreprise et la catégorie en une seule requête SQL
    offres = Jobs.objects.all().select_related('company', 'category').order_with_respect_to('id')[:6]
    
    # 2. On envoie les données au fichier HTML sous forme de dictionnaire (contexte)
    context = {
        'offres': offres
    }

    return render(request, 'jobs/accueil.html', context)

