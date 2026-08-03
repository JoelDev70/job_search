from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("jobs", "0007_application_documents_and_company_logo")]

    operations = [
        migrations.AddField(model_name="companies", name="is_approved", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="jobs", name="attachment", field=models.FileField(blank=True, max_length=255, null=True, upload_to="jobs/attachments/")),
        migrations.AddField(model_name="applications", name="interview_at", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="applications", name="meeting_at", field=models.DateTimeField(blank=True, null=True)),
    ]
