# Generated by Django 5.0.4 on 2024-04-24 18:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("med_ai_api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patient",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="height",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="symptoms",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="weight",
        ),
    ]
