from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from jobs.models import Applications, Jobs

from .forms import ProfileForm
from .models import Profiles, Users
from .services import notify

PUBLIC_ROLES = {"JOB_SEEKER", "RECRUITER"}


def connexion(request):
    if request.session.get("user_id"):
        return redirect("accueil")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = Users.objects.filter(username=username, is_active__in=(1, True)).first()
        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["user_role"] = user.role
            if user.role == "JOB_SEEKER":
                return redirect("dashboard_candidat")
            return redirect(request.GET.get("next", "dashboard_recruteur" if user.role == "RECRUITER" else "accueil"))
        messages.error(request, "Identifiants invalides.")
    return render(request, "accounts/connexion.html")


def inscription(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "JOB_SEEKER")
        if not username or not email or len(password) < 8 or role not in PUBLIC_ROLES:
            messages.error(request, "Renseignez tous les champs et utilisez un mot de passe d'au moins 8 caractères.")
            return render(request, "accounts/inscription.html")
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Saisissez une adresse e-mail valide.")
            return render(request, "accounts/inscription.html")

        # ADMIN ne peut pas être choisi dans un formulaire public.
        # La base impose les valeurs enum ADMIN, RECRUITER et JOB_SEEKER.
        # La création du profil dans la même transaction évite un compte incomplet.
        if Users.objects.filter(username=username).exists() or Users.objects.filter(email=email).exists():
            messages.error(request, "Ce nom d'utilisateur ou cet e-mail existe déjà.")
        else:
            now = timezone.now()
            with transaction.atomic():
                user = Users.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    role=role,
                    is_active=1,
                    first_name="",
                    last_name="",
                    created_at=now,
                    updated_at=now,
                )
                Profiles.objects.create(user=user, created_at=now, updated_at=now)
            if role == "JOB_SEEKER":
                notify(user, "Bienvenue sur Job Search", "Bienvenue ! Votre compte candidat est prêt. Découvrez les offres et postulez dès maintenant.")
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["user_role"] = user.role
            return redirect("dashboard_candidat" if role == "JOB_SEEKER" else "profile_recruteur")
    return render(request, "accounts/inscription.html")


def deconnexion(request):
    request.session.flush()
    return redirect("accueil")


def profil(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("connexion")
    user = Users.objects.get(id=user_id)
    if user.role == "RECRUITER":
        return redirect("profile_recruteur")
    profile, _ = Profiles.objects.get_or_create(user=user, defaults={"created_at": timezone.now(), "updated_at": timezone.now()})
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.updated_at = timezone.now()
        profile.save()
        messages.success(request, "Votre profil a été enregistré.")
        return redirect("dashboard_candidat" if user.role == "JOB_SEEKER" else "profil")
    return render(request, "accounts/profil.html", {"user": user, "profile": profile, "form": form})


def dashboard_candidat(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("connexion")
    user = get_object_or_404(Users, id=user_id)
    if user.role != "JOB_SEEKER":
        messages.error(request, "Ce tableau de bord est réservé aux candidats.")
        return redirect("accueil")

    applications = Applications.objects.filter(user=user).select_related("job__company").order_by("-application_date")
    applied_job_ids = applications.values_list("job_id", flat=True)
    recommended_job = Jobs.objects.filter(status__in=("published", "active")).filter(Q(deadline__isnull=True) | Q(deadline__gte=timezone.localdate())).exclude(id__in=applied_job_ids).select_related("company").order_by("-created_at").first()
    profile, _ = Profiles.objects.get_or_create(user=user, defaults={"created_at": timezone.now(), "updated_at": timezone.now()})
    filled_fields = [user.phone, profile.city, profile.education, profile.bio, profile.photo]
    completion = 20 + (sum(bool(value) for value in filled_fields) * 16)
    return render(request, "accounts/dashboard_candidat.html", {"user": user, "profile": profile, "applications": applications[:8], "applications_count": applications.count(), "interviews_count": applications.filter(status="INTERVIEW").count(), "completion": completion, "recommended_job": recommended_job})
