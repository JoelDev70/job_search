from django import forms

from .models import Applications, Jobs


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ["cover_letter", "cv"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 7, "placeholder": "Présentez votre motivation..."}),
            "cv": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Lien vers votre CV (PDF)"}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ["company", "category", "title", "description", "city", "province", "country", "contract_type", "salary_min", "salary_max", "experience_required", "education_required", "vacancies", "deadline", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 7}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
        }

    def clean(self):
        cleaned = super().clean()
        minimum, maximum = cleaned.get("salary_min"), cleaned.get("salary_max")
        if minimum is not None and maximum is not None and minimum > maximum:
            self.add_error("salary_max", "Le salaire maximum doit être supérieur au minimum.")
        return cleaned
