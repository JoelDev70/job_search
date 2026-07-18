from django.db import models



class Notifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    title = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notifications'


class ProfileSkills(models.Model):
    pk = models.CompositePrimaryKey('profile_id', 'skill_id')
    profile = models.ForeignKey('Profiles', models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    level = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile_skills'


class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    # user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE) # <-- Remplacez 'Users' ou 'jobs.Users' par 'accounts.Users'

    user = models.OneToOneField('Users', models.DO_NOTHING)
    date_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=150, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'profiles'


class Skills(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
