from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("accounts", "0002_alter_notifications_options_alter_profiles_options_and_more")]

    operations = [
        migrations.AlterModelOptions(name="notifications", options={"managed": True, "verbose_name": "Notification", "verbose_name_plural": "Notifications"}),
        migrations.AlterModelOptions(name="profiles", options={"managed": True, "verbose_name": "Profile", "verbose_name_plural": "Profiles"}),
        migrations.AlterModelOptions(name="profileskills", options={"managed": True}),
        migrations.AlterModelOptions(name="skills", options={"managed": True, "verbose_name": "Skill", "verbose_name_plural": "Skills"}),
        migrations.AlterModelOptions(name="users", options={"managed": True, "verbose_name": "User", "verbose_name_plural": "Users"}),
    ]
