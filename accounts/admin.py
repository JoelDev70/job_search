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
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'role', 'is_active', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active')
    actions = ('ban_accounts', 'unban_accounts')
    search_fields = ('username', 'email')

    @admin.action(description="Bannir les comptes sélectionnés")
    def ban_accounts(self, request, queryset):
        queryset.exclude(role="ADMIN").update(is_active=0)

    @admin.action(description="Réactiver les comptes sélectionnés")
    def unban_accounts(self, request, queryset):
        queryset.update(is_active=1)
