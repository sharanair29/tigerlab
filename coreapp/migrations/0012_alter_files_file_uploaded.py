# Generated by Django 4.1.7 on 2023-02-16 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coreapp", "0011_alter_files_file_uploaded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="files",
            name="file_uploaded",
            field=models.FileField(upload_to="files"),
        ),
    ]
