# Generated by Django 4.1.7 on 2023-02-15 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("coreapp", "0006_teamscore_file_alter_teamscore_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teamscore",
            name="file",
        ),
        migrations.RemoveField(
            model_name="teamscore",
            name="user",
        ),
    ]
