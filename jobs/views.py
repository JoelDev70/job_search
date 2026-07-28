from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, JobForm
from .models import Applications, Categories, Companies, Jobs
from accounts.models import Users


def _published_jobs():
    return Jobs.objects.filter(status__in=("published", "active")).select_related("company", "category")


def accueil_job_board(request):
    return render(request, "jobs/accueil_jobsearch.html", {"offres": _published_jobs().order_by("-created_at")[:6]})


def lister_offres(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    offres = _published_jobs().order_by("-created_at")
    if query:
        offres = offres.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(company__company_name__icontains=query))
    if category:
        offres = offres.filter(category_id=category)
    return render(request, "jobs/recherche_d_offres.html", {"categories": Categories.objects.all(), "offres": offres, "query": query, "selected_category": category})


def detail_offre(request, id):
    offre = get_object_or_404(Jobs.objects.select_related("company", "category"), id=id)
    return render(request, "jobs/detail_offre.html", {"offre": offre})


def profile_entreprise(request):
    return render(request, "jobs/profile_entreprise.html", {"companies": Companies.objects.all(), "offres": _published_jobs()})


def _require_account(request):
    if not request.session.get("user_id"):
        return redirect(f"/accounts/connexion/?next={request.path}")
    return None


def ajouter_offre(request):
    redirect_response = _require_account(request)
    if redirect_response:
        return redirect_response
    user = get_object_or_404(Users, id=request.session["user_id"])
    if user.role not in ("ADMIN", "RECRUITER"):
        messages.error(request, "Seuls les recruteurs peuvent publier une offre.")
        return redirect("liste_offres")
    form = JobForm(request.POST or None)
    form.fields["company"].queryset = Companies.objects.filter(recruiter=user)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.created_at = timezone.now()
        job.updated_at = timezone.now()
        job.save()
        messages.success(request, "L'offre a été publiée avec succès.")
        return redirect("detail_offre", id=job.id)
    return render(request, "jobs/offre_form.html", {"form": form, "page_title": "Publier une offre"})


def modifier_offre(request, id):
    redirect_response = _require_account(request)
    if redirect_response:
        return redirect_response
    job = get_object_or_404(Jobs, id=id)
    user = get_object_or_404(Users, id=request.session["user_id"])
    if user.role != "ADMIN" and job.company.recruiter_id != user.id:
        messages.error(request, "Vous ne pouvez modifier que les offres de votre entreprise.")
        return redirect("detail_offre", id=job.id)
    form = JobForm(request.POST or None, instance=job)
    if user.role != "ADMIN":
        form.fields["company"].queryset = Companies.objects.filter(recruiter=user)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.updated_at = timezone.now()
        job.save()
        messages.success(request, "L'offre a été modifiée.")
        return redirect("detail_offre", id=job.id)
    return render(request, "jobs/offre_form.html", {"form": form, "page_title": "Modifier l'offre", "job": job})


@require_POST
def supprimer_offre(request, id):
    redirect_response = _require_account(request)
    if redirect_response:
        return redirect_response
    job = get_object_or_404(Jobs, id=id)
    user = get_object_or_404(Users, id=request.session["user_id"])
    if user.role != "ADMIN" and job.company.recruiter_id != user.id:
        messages.error(request, "Vous ne pouvez supprimer que les offres de votre entreprise.")
        return redirect("detail_offre", id=job.id)
    job.delete()
    messages.success(request, "L'offre a été supprimée.")
    return redirect("liste_offres")


def postuler_offre(request, id):
    job = get_object_or_404(Jobs, id=id)
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect(f"/accounts/connexion/?next=/offre/{job.id}/postuler/")
    user = get_object_or_404(Users, id=user_id)
    if user.role != "JOB_SEEKER":
        messages.error(request, "Seuls les candidats peuvent envoyer une candidature.")
        return redirect("detail_offre", id=job.id)
    if Applications.objects.filter(user=user, job=job).exists():
        messages.info(request, "Vous avez déjà postulé à cette offre.")
        return redirect("detail_offre", id=job.id)
    form = ApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.user = user
        application.job = job
        application.application_date = timezone.now()
        application.status = "PENDING"
        application.save()
        messages.success(request, "Votre candidature a été envoyée.")
        return redirect("detail_offre", id=job.id)
    return render(request, "jobs/postuler.html", {"form": form, "offre": job})
