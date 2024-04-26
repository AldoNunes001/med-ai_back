# Generated by Django 5.0.4 on 2024-04-26 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("med_ai_api", "0003_patient_created_at_patient_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicalRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notes", models.FileField(blank=True, upload_to="medical_records/")),
                (
                    "patient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medical_record",
                        to="med_ai_api.patient",
                    ),
                ),
            ],
        ),
    ]
