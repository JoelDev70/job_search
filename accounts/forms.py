from django import forms

from .models import Profiles


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ["date_birth", "gender", "address", "city", "province", "country", "education", "experience_years", "expected_salary", "availability", "bio", "photo"]
        widgets = {
            "date_birth": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
            "gender": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "address": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "city": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "province": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "country": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "education": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "experience_years": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": 0}),
            "expected_salary": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": 0, "step": "0.01"}),
            "availability": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "bio": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 5}),
            "photo": forms.ClearableFileInput(attrs={"class": "file-input file-input-bordered w-full", "accept": "image/*"}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if not photo:
            return photo
        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La photo ne doit pas dépasser 5 Mo.")
        content_type = getattr(photo, "content_type", "")
        if content_type and not content_type.startswith("image/"):
            raise forms.ValidationError("Choisissez un fichier image.")
        return photo
