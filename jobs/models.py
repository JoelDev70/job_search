from django.db import models
from accounts.models import Users, Skills
from django.utils import timezone

# Create your models here.
class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = 'categories'
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'


class Companies(models.Model):
    id = models.BigAutoField(primary_key=True)
    recruiter = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.FileField(upload_to="companies/logos/", max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.company_name

    @property
    def logo_url(self):
        """Prend aussi en charge les anciens logos enregistrés comme URL."""
        if not self.logo:
            return ""
        if self.logo.name.startswith(("http://", "https://")):
            return self.logo.name
        return self.logo.url
    
    class Meta:
        managed = True
        db_table = 'companies'
        verbose_name = 'Compagnie'
        verbose_name_plural = 'Compagnies'


class Applications(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "En attente"),
        ("UNDER_REVIEW", "En cours d'examen"),
        ("INTERVIEW", "Entretien"),
        ("ACCEPTED", "Acceptée"),
        ("REJECTED", "Refusée"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    job = models.ForeignKey('Jobs', models.DO_NOTHING)
    application_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="PENDING")
    matching_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cv = models.FileField(upload_to="applications/cv/", max_length=255, blank=True, null=True)
    # Colonne texte conservée pour ne pas tronquer les anciennes lettres saisies.
    # Les nouvelles candidatures y enregistrent le chemin du PDF téléversé.
    cover_letter = models.TextField(blank=True, null=True)
    interview_at = models.DateTimeField(blank=True, null=True)
    meeting_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        managed = True
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

class JobSkills(models.Model):
    pk = models.CompositePrimaryKey('job_id', 'skill_id')
    job = models.ForeignKey('Jobs', models.DO_NOTHING)
    skill = models.ForeignKey('accounts.Skills', on_delete=models.CASCADE)
    required = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'job_skills'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    contract_type = models.CharField(max_length=100, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    experience_required = models.IntegerField(blank=True, null=True)
    education_required = models.CharField(max_length=100, blank=True, null=True)
    vacancies = models.IntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="published")
    attachment = models.FileField(upload_to="jobs/attachments/", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        managed = True
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
