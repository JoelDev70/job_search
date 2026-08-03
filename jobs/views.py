from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, CompanyForm, JobForm
from accounts.forms import RecruiterAccountForm
from .models import Applications, Categories, Companies, Jobs
from accounts.models import Users


def _published_jobs():
    return Jobs.objects.filter(
        status__in=("published", "active")
    ).filter(
        Q(deadline__isnull=True) | Q(deadline__gte=timezone.localdate())
    ).select_related("company", "category")


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
    paginator = Paginator(offres, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "jobs/recherche_d_offres.html", {"categories": Categories.objects.all(), "page_obj": page_obj, "offres": page_obj.object_list, "query": query, "selected_category": category})


def detail_offre(request, id):
    offre = get_object_or_404(Jobs.objects.select_related("company", "category"), id=id)
    user_id = request.session.get("user_id")
    owner = user_id and (offre.company.recruiter_id == user_id or get_object_or_404(Users, id=user_id).role == "ADMIN")
    if offre.deadline and offre.deadline < timezone.localdate() and not owner:
        messages.info(request, "Cette offre a expiré.")
        return redirect("liste_offres")
    return render(request, "jobs/detail_offre.html", {"offre": offre, "is_expired": bool(offre.deadline and offre.deadline < timezone.localdate())})


def profile_entreprise(request):
    return render(request, "jobs/profile_entreprise.html", {"companies": Companies.objects.all(), "offres": _published_jobs()})


def _require_account(request):
    if not request.session.get("user_id"):
        return redirect(f"/accounts/connexion/?next={request.path}")
    return None


def _recruiter_user(request):
    """Retourne le recruteur connecté ou une redirection adaptée."""
    redirect_response = _require_account(request)
    if redirect_response:
        return None, redirect_response
    user = get_object_or_404(Users, id=request.session["user_id"])
    if user.role not in ("ADMIN", "RECRUITER"):
        messages.error(request, "Cet espace est réservé aux recruteurs.")
        return None, redirect("liste_offres")
    return user, None


def dashboard_recruteur(request):
    user, redirect_response = _recruiter_user(request)
    if redirect_response:
        return redirect_response

    companies = Companies.objects.filter(recruiter=user)
    jobs = Jobs.objects.filter(company__in=companies).select_related("company").order_by("-created_at")
    applications = Applications.objects.filter(job__company__in=companies).select_related("user", "job__company").order_by("-application_date")
    return render(request, "jobs/dashboard_recruteur.html", {
        "user": user,
        "company": companies.first(),
        "active_jobs_count": jobs.filter(status__in=("published", "active")).count(),
        "jobs_count": jobs.count(),
        "applications_count": applications.count(),
        "pending_applications_count": applications.filter(status__in=("PENDING", "UNDER_REVIEW")).count(),
        "interviews_count": applications.filter(status="INTERVIEW").count(),
        "recent_applications": applications[:6],
        "recent_jobs": jobs.annotate(applications_total=Count("applications")).all()[:5],
        "expired_jobs": jobs.filter(deadline__lt=timezone.localdate()).annotate(applications_total=Count("applications")),
    })


def profile_recruteur(request):
    user, redirect_response = _recruiter_user(request)
    if redirect_response:
        return redirect_response
    company = Companies.objects.filter(recruiter=user).first()
    account_form = RecruiterAccountForm(instance=user, prefix="account")
    company_form = CompanyForm(instance=company, prefix="company")

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "account":
            account_form = RecruiterAccountForm(request.POST, instance=user, prefix="account")
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.updated_at = timezone.now()
                account.save()
                messages.success(request, "Vos coordonnées de recruteur ont été enregistrées.")
                return redirect("profile_recruteur")
        elif form_type == "company":
            company_form = CompanyForm(request.POST, request.FILES, instance=company, prefix="company")
            if company_form.is_valid():
                saved_company = company_form.save(commit=False)
                saved_company.recruiter = user
                saved_company.updated_at = timezone.now()
                if not saved_company.pk:
                    saved_company.created_at = timezone.now()
                saved_company.save()
                messages.success(request, "Votre entreprise est maintenant prête à publier des offres.")
                return redirect("dashboard_recruteur")
        else:
            messages.error(request, "La demande est invalide.")
    return render(request, "jobs/profile_recruteur.html", {"user": user, "company": company, "account_form": account_form, "company_form": company_form})


def ajouter_offre(request):
    redirect_response = _require_account(request)
    if redirect_response:
        return redirect_response
    user = get_object_or_404(Users, id=request.session["user_id"])
    if user.role not in ("ADMIN", "RECRUITER"):
        messages.error(request, "Seuls les recruteurs peuvent publier une offre.")
        return redirect("liste_offres")
    if user.role == "RECRUITER" and not Companies.objects.filter(recruiter=user).exists():
        messages.info(request, "Créez d'abord votre entreprise avant de publier une offre.")
        return redirect("profile_recruteur")
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
    if job.deadline and job.deadline < timezone.localdate():
        messages.error(request, "La date limite de cette offre est dépassée.")
        return redirect("liste_offres")
    form = ApplicationForm(request.POST or None, request.FILES or None)
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


@require_POST
def modifier_statut_candidature(request, id):
    user, redirect_response = _recruiter_user(request)
    if redirect_response:
        return redirect_response
    application = get_object_or_404(Applications.objects.select_related("job__company"), id=id)
    if user.role != "ADMIN" and application.job.company.recruiter_id != user.id:
        messages.error(request, "Vous ne pouvez gérer que les candidatures de votre entreprise.")
        return redirect("dashboard_recruteur")
    status = request.POST.get("status")
    allowed_statuses = dict(Applications.STATUS_CHOICES)
    if status not in allowed_statuses:
        messages.error(request, "Statut invalide.")
    else:
        application.status = status
        application.save(update_fields=["status"])
        messages.success(request, "Le statut de la candidature a été mis à jour.")
    return redirect("dashboard_recruteur")
