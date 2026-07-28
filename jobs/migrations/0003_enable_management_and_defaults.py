from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [("jobs", "0002_alter_applications_options_alter_categories_options_and_more")]

    operations = [
        migrations.AlterModelOptions(name="applications", options={"managed": True, "verbose_name": "Application", "verbose_name_plural": "Applications"}),
        migrations.AlterModelOptions(name="categories", options={"managed": True, "verbose_name": "Categorie", "verbose_name_plural": "Categories"}),
        migrations.AlterModelOptions(name="companies", options={"managed": True, "verbose_name": "Compagnie", "verbose_name_plural": "Compagnies"}),
        migrations.AlterModelOptions(name="jobs", options={"managed": True, "verbose_name": "Job", "verbose_name_plural": "Jobs"}),
        migrations.AlterModelOptions(name="jobskills", options={"managed": True}),
        migrations.AlterField(model_name="jobs", name="status", field=models.CharField(default="published", max_length=20)),
        migrations.AlterField(model_name="jobs", name="created_at", field=models.DateTimeField(default=timezone.now, editable=False)),
        migrations.AlterField(model_name="jobs", name="updated_at", field=models.DateTimeField(default=timezone.now)),
    ]
