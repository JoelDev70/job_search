from django import forms
from django.core.files.storage import default_storage

from .models import Applications, Companies, Jobs


class ApplicationForm(forms.ModelForm):
    cover_letter = forms.FileField(
        label="Lettre de motivation (PDF)",
        widget=forms.ClearableFileInput(attrs={"class": "block w-full rounded-lg border border-[#c6c6cd] p-2", "accept": "application/pdf,.pdf"}),
    )
    class Meta:
        model = Applications
        fields = ["cv", "cover_letter"]
        widgets = {
            "cv": forms.ClearableFileInput(attrs={"class": "block w-full rounded-lg border border-[#c6c6cd] p-2", "accept": "application/pdf,.pdf"}),
        }

    def clean(self):
        cleaned = super().clean()
        for field in ("cv", "cover_letter"):
            document = cleaned.get(field)
            if not document:
                self.add_error(field, "Ce document PDF est obligatoire.")
                continue
            if getattr(document, "size", 0) > 5 * 1024 * 1024:
                self.add_error(field, "Le fichier ne doit pas dépasser 5 Mo.")
            name = getattr(document, "name", "").lower()
            content_type = getattr(document, "content_type", "")
            if not name.endswith(".pdf") or (content_type and content_type != "application/pdf"):
                self.add_error(field, "Choisissez un fichier PDF.")
        return cleaned

    def save(self, commit=True):
        application = super().save(commit=False)
        document = self.cleaned_data["cover_letter"]
        application.cover_letter = default_storage.save("applications/cover_letters/" + document.name, document)
        if commit:
            application.save()
        return application


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ["company", "category", "title", "description", "city", "province", "country", "contract_type", "salary_min", "salary_max", "experience_required", "education_required", "vacancies", "deadline", "attachment", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 7}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
            "attachment": forms.ClearableFileInput(attrs={"class": "block w-full rounded-lg border border-[#c6c6cd] p-2", "accept": "application/pdf,.pdf"}),
        }

    def clean(self):
        cleaned = super().clean()
        minimum, maximum = cleaned.get("salary_min"), cleaned.get("salary_max")
        if minimum is not None and maximum is not None and minimum > maximum:
            self.add_error("salary_max", "Le salaire maximum doit être supérieur au minimum.")
        return cleaned

    def clean_attachment(self):
        document = self.cleaned_data.get("attachment")
        if not document:
            return document
        if document.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Le document ne doit pas dépasser 5 Mo.")
        if not document.name.lower().endswith(".pdf") or (getattr(document, "content_type", "") and document.content_type != "application/pdf"):
            raise forms.ValidationError("Choisissez un document PDF.")
        return document


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
            "logo": forms.ClearableFileInput(attrs={"class": "w-full rounded-lg border-[#c6c6cd] px-3 py-2 focus:border-[#006c49] focus:ring-[#006c49]", "accept": "image/*"}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if not logo:
            return logo
        if logo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Le logo ne doit pas dépasser 5 Mo.")
        if getattr(logo, "content_type", "") and not logo.content_type.startswith("image/"):
            raise forms.ValidationError("Choisissez un fichier image.")
        return logo
