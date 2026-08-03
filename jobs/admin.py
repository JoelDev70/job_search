from django.contrib import admin
# Register your models here.
from .models import Applications, Categories, Companies,  Jobs # Assurez-vous que les noms correspondent à vos classes

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description') 
    search_fields = ('name',)

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('id','recruiter','company_name','is_approved','email','phone','city','country','created_at','updated_at')
    list_filter = ('is_approved',)
    actions = ('approve_companies',)
    search_fields = ('company_name', 'city')

    @admin.action(description="Valider les entreprises sélectionnées")
    def approve_companies(self, request, queryset):
        queryset.update(is_approved=True)
    
    
@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id','user','job','application_date','status','interview_at','meeting_at','matching_score','cv','cover_letter')
    search_fields = ('user', 'job')
    
# @admin.register(JobSkills)
# class JobSkillsAdmin(admin.ModelAdmin):
#     list_display = ('id','pk','job','skill','required')
#     search_fields = ('job', 'skill')

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ('id','company','category','title','city','contract_type','deadline','attachment','status','created_at','updated_at')
    search_fields = ('company', 'title')
