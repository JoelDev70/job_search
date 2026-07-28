from django.db import models



class Notifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    title = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title or "Notification"

    class Meta:
        managed = True
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class ProfileSkills(models.Model):
    pk = models.CompositePrimaryKey('profile_id', 'skill_id')
    profile = models.ForeignKey('Profiles', models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    level = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return str(self.skill)

    class Meta:
        managed = True
        db_table = 'profile_skills'


class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    # user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE) # <-- Remplacez 'Users' ou 'jobs.Users' par 'accounts.Users'

    user = models.OneToOneField('Users', models.DO_NOTHING)
    date_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (
        ("MALE", "Homme"),
        ("FEMALE", "Femme"),
        ("OTHER", "Autre"),
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=150, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to="profiles/", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        """Fonctionne aussi avec les anciennes photos enregistrées comme URL."""
        if not self.photo:
            return ""
        if self.photo.name.startswith(("http://", "https://")):
            return self.photo.name
        return self.photo.url

    class Meta:
        managed = True
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Skills(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'skills'
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Users(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "Administrateur"),
        ("RECRUITER", "Recruteur"),
        ("JOB_SEEKER", "Candidat"),
    )

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="JOB_SEEKER")
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
