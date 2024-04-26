from django.conf import settings
from django.db import models


class Patient(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)  # Opcional
    weight = models.FloatField(null=True, blank=True)  # Opcional
    height = models.FloatField(null=True, blank=True)  # Opcional
    symptoms = models.TextField(blank=True)  # Opcional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="patients"
    )

    def __str__(self) -> str:
        return self.name


class MedicalRecord(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="medical_record"
    )
    notes = models.FileField(upload_to='medical_records/', blank=True)

    def __str__(self) -> str:
        return f"MR -> {self.patient.name}"
