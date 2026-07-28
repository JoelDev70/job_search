from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0004_merge_20260727_1057")]

    operations = [
        migrations.AlterModelOptions(name="notifications", options={"managed": True, "verbose_name": "Notification", "verbose_name_plural": "Notifications"}),
        migrations.AlterModelOptions(name="profiles", options={"managed": True, "verbose_name": "Profile", "verbose_name_plural": "Profiles"}),
        migrations.AlterModelOptions(name="skills", options={"managed": True, "verbose_name": "Skill", "verbose_name_plural": "Skills"}),
        migrations.AlterModelOptions(name="users", options={"managed": True, "verbose_name": "User", "verbose_name_plural": "Users"}),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(model_name="notifications", name="user", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="accounts.users")),
                migrations.AddField(model_name="profiles", name="user", field=models.OneToOneField(on_delete=models.DO_NOTHING, to="accounts.users")),
                migrations.AddField(model_name="profileskills", name="profile", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="accounts.profiles")),
                migrations.AddField(model_name="profileskills", name="skill", field=models.ForeignKey(on_delete=models.DO_NOTHING, to="accounts.skills")),
            ],
            database_operations=[],
        )
    ]
