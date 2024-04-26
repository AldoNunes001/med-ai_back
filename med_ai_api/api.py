from typing import List
from django.shortcuts import get_object_or_404
from .models import MedicalRecord, Patient
from .schema import PatientAddSchema, PatientResponseSchema, NotFoundError
from django.contrib.auth import get_user_model
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI, api_controller, route
from ninja import File
from ninja.files import UploadedFile

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


@api_controller("/patients", tags=["patients"], permissions=[])
class PatientController:
    @route.get("/", response={200: List[PatientResponseSchema]}, auth=JWTAuth())
    def list_patients(self):
        patients = Patient.objects.all()
        return patients

    @route.get("/{cpf}", response={200: PatientResponseSchema, 404: NotFoundError}, auth=JWTAuth())
    def get_patient(self, cpf: str):
        try:
            patient = Patient.objects.get(cpf=cpf)
            name = patient.name
            cpf = patient.cpf
            return {"name": name, "cpf": cpf}
        except Patient.DoesNotExist:
            return (404, {"message": "Paciente não encontrado"})

    @route.post("/", response={200: PatientResponseSchema}, auth=JWTAuth())
    def save_patient(self, patient_data: PatientAddSchema):
        User = get_user_model()
        user = User.objects.get(username=patient_data.username)
        patient, created = Patient.objects.update_or_create(
            cpf=patient_data.cpf,
            defaults={"name": patient_data.name, "created_by": user},
        )
        return patient


@api_controller("/mr", tags=["medical_records"], permissions=[])
class MedicalRecordController:

    @route.post("/upload", response={200: str}, auth=JWTAuth())
    def upload_file(self, patient_id: int, file: UploadedFile = File(...)):
        patient = get_object_or_404(Patient, pk=patient_id)
        
        medical_record, created = MedicalRecord.objects.get_or_create(
            patient=patient,
            defaults={'notes': file}
        )

        if not created:
            medical_record.notes = file
            medical_record.save()
        
        return "Arquivo salvo com sucesso"


api.register_controllers(MedicalRecordController)
api.register_controllers(PatientController)
