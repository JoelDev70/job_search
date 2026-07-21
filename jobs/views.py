from django.shortcuts import render, redirect, get_object_or_404
from .models import Jobs, Companies, Categories  # Adaptez les noms exacts de vos classes
# from .forms import JobForm

def accueil_job_board(request):
    # 1. On récupère toutes les offres d'emploi enregistrées dans XAMPP
    # .select_related() permet de charger l'entreprise et la catégorie en une seule requête SQL
    offres = Jobs.objects.all().select_related('company', 'category')
    # 2. On envoie les données au fichier HTML sous forme de dictionnaire (contexte)
    context = {
        'offres': offres
    }
    return render(request, 'jobs/accueil_jobsearch.html', context)

def lister_offres(request):
    offres = Jobs.objects.all().select_related('company', 'category')
    categories = Categories.objects.all()
    context = {
        'categories': categories,
        'offres': offres
    }
    return render(request, 'jobs/recherche_d_offres.html',context)
# jobsearch




def ajouter_offre(request):
    if request.method == "POST":
        # 1. On récupère les textes et les IDs des clés étrangères
        title = request.POST.get('title')
        description = request.POST.get('description')
        salary = request.POST.get('salary')
        company_id = request.POST.get('company')
        category_id = request.POST.get('category')
        
        # 2. On récupère les vrais objets de la base de données
        company_obj = get_object_or_404(Companies, id=company_id)
        category_obj = get_object_or_404(Categories, id=category_id)
        
        # 3. On crée l'offre d'emploi liée
        Jobs.objects.create(
            title=title,
            description=description,
            salary=salary,
            company=company_obj,      # Liaison SQL
            category=category_obj     # Liaison SQL
        )
        return redirect('accueil')  # Redirige vers votre page d'accueil
        
    # Pour afficher le formulaire, on a besoin de lister toutes les entreprises et catégories
    companies = Companies.objects.all()
    categories = Categories.objects.all()
    return render(request, 'jobs/offre_form.html', {'companies': companies, 'categories': categories})


# MODIFIER UNE OFFRE EXISTANTE
def modifier_offre(request, id):
    job = get_object_or_404(Jobs, id=id)
    if request.method == "POST":
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.salary = request.POST.get('salary')
        job.company = get_object_or_404(Companies, id=request.POST.get('company'))
        job.category = get_object_or_404(Categories, id=request.POST.get('category'))
        job.save()
        return redirect('accueil')
        
    companies = Companies.objects.all()
    categories = Categories.objects.all()
    return render(request, 'jobs/offre_form.html', {'job': job, 'companies': companies, 'categories': categories})

# SUPPRIMER UNE OFFRE
def supprimer_offre(request, id):
    job = get_object_or_404(Jobs, id=id)
    job.delete()
    return redirect('accueil')
