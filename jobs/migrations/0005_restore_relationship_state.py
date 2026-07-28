from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("jobs", "0004_merge_20260727_1056")]

    operations = [
        migrations.AlterModelOptions(name="applications", options={"managed": True, "verbose_name": "Application", "verbose_name_plural": "Applications"}),
        migrations.AlterModelOptions(name="categories", options={"managed": True, "verbose_name": "Categorie", "verbose_name_plural": "Categories"}),
        migrations.AlterModelOptions(name="companies", options={"managed": True, "verbose_name": "Compagnie", "verbose_name_plural": "Compagnies"}),
        migrations.AlterModelOptions(name="jobs", options={"managed": True, "verbose_name": "Job", "verbose_name_plural": "Jobs"}),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(model_name="applications", name="user", field=models.ForeignKey(on_delete=models.CASCADE, to="accounts.users")),
                migrations.AddField(model_name="applications", name="job", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="jobs.jobs")),
                migrations.AddField(model_name="companies", name="recruiter", field=models.ForeignKey(on_delete=models.CASCADE, to="accounts.users")),
                migrations.AddField(model_name="jobs", name="company", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="jobs.companies")),
                migrations.AddField(model_name="jobs", name="category", field=models.ForeignKey(blank=True, null=True, on_delete=models.DO_NOTHING, to="jobs.categories")),
                migrations.AddField(model_name="jobskills", name="job", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="jobs.jobs")),
                migrations.AddField(model_name="jobskills", name="skill", field=models.ForeignKey(on_delete=models.CASCADE, to="accounts.skills")),
            ],
            database_operations=[],
        )
    ]
