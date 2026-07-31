from django import forms

from .models import Applications, Companies, Jobs


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


class CompanyForm(forms.ModelForm):
    """Informations publiques et de contact de l'entreprise du recruteur."""

    class Meta:
        model = Companies
        fields = ["company_name", "email", "phone", "website", "address", "city", "country", "description", "logo"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "placeholder": "Nom de l'entreprise"}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "placeholder": "contact@entreprise.com"}),
            "phone": forms.TextInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]"}),
            "website": forms.URLInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "placeholder": "https://www.entreprise.com"}),
            "address": forms.TextInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]"}),
            "city": forms.TextInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]"}),
            "country": forms.TextInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]"}),
            "description": forms.Textarea(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "rows": 5, "placeholder": "Présentez votre entreprise, sa mission et sa culture..."}),
            "logo": forms.URLInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "placeholder": "URL du logo (facultatif)"}),
        }
