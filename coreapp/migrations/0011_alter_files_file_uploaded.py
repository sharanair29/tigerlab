# Generated by Django 4.1.7 on 2023-02-16 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coreapp", "0010_alter_teamscore_file_alter_teamscore_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="files",
            name="file_uploaded",
            field=models.FileField(upload_to="media/files"),
        ),
    ]