from django import forms
from .models import Applications,Jobs

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ["user","job","application_date","status","matching_score","cv","cover_letter"]
        widgets = {
            'user' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'User'
            }),
            'job' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Job'
            }),
            'application_date' : forms.DateInput(attrs={
                'class' : 'input w-full',
                'placeholder' : '18-07-2026'
            }),
            'status' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Status'
            })
            ,
            'matching_score' : forms.NumberInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Score'
            }),
            'cv' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Cv'
            }),
            'cover_letter' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'cover'
            }),
        }
        
        

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ["company","category","title","description","city","province","country","contract_type","salary_min","salary_max","experience_required","education_required","vacancies","deadline","status","created_at","updated_at"]
        widgets = {
            'company' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Company'
            }),
            'category' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Category'
            }),
            'title' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'title'
            }),
            'description' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Description'
            })
            ,
            'city' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'City'
            }),
            'province' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Province'
            }),
            'country' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'country'
            }),
            'contract_type' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Contract_type'
            }),
            'salary_min' : forms.NumberInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Min'
            }),
            'salary_max' : forms.NumberInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Max'
            }),
            'experience_required' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Experience'
            })
            ,
            'education_required' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Education'
            }),
            'vacancies' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Vacancie'
            }),
            'deadline' : forms.TimeInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Deadline'
            }),
            'status' : forms.TextInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Status'
            }),
            'ceated_at' : forms.TimeInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'created'
            }),
            'updated_at' : forms.TimeInput(attrs={
                'class' : 'input w-full',
                'placeholder' : 'Updated'
            }),
        }