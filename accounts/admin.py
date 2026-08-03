from django.contrib import admin
from .models import Notifications, Profiles, Skills, Users # Assurez-vous que les noms correspondent à vos classes

# Register your models here.
@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'message', 'is_read', 'created_at')
    search_fields = ('user', 'title')


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_birth', 'gender', 'address', 'city', 'province', 'country', 'education', 'experience_years', 'expected_salary', 'availability', 'bio', 'photo', 'created_at', 'updated_at')
    search_fields = ('user', 'city')

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description')
    search_fields = ('name',)
    
    
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email','password', 'phone', 'role', 'is_active', 'created_at', 'updated_at')
    search_fields = ('username', 'email')