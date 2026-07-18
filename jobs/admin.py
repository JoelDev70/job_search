from django.contrib import admin
# Register your models here.
from .models import Applications, Categories, Companies,  Jobs # Assurez-vous que les noms correspondent à vos classes

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description') 
    search_fields = ('name',)

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('id','recruiter','company_name','email','phone','website','address','city','country','description','logo','created_at','updated_at')
    search_fields = ('company_name', 'city')
    
    
@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id','user','job','application_date','status','matching_score','cv','cover_letter')
    search_fields = ('user', 'job')
    
# @admin.register(JobSkills)
# class JobSkillsAdmin(admin.ModelAdmin):
#     list_display = ('id','pk','job','skill','required')
#     search_fields = ('job', 'skill')

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ('id','company','category','title','description','city','province','country','contract_type','salary_min','salary_max','experience_required','education_required','vacancies','deadline','status','created_at','updated_at')
    search_fields = ('company', 'title')