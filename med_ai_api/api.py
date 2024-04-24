# from typing import Any
# from django.contrib.auth import authenticate as auth_authenticate
# from django.contrib.auth import login as auth_login
# from django.http import HttpRequest
# from django.contrib.auth.models import User
from typing import List
from .models import Patient
# from ninja import NinjaAPI
# from ninja.security import HttpBearer, HttpBasicAuth
# import jwt
from .schema import PatientResponseSchema, UserSchema, UserResponseSchema, NotAuthenticatedError, NotFoundError

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI, api_controller, route

# api = NinjaAPI()
api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

JWT_SECRET = "diogofredoferreira"


@api_controller('/patients', tags=['patients'], permissions=[])
class PatientController:

    @route.get('/', response={200: List[PatientResponseSchema]})
    def list_patients(self):
        patients = Patient.objects.all()
        return patients

    @route.get('/{cpf}', response={200: PatientResponseSchema, 404: NotFoundError}, auth=JWTAuth())
    def get_patient(self, cpf: str):
        try:
            patient = Patient.objects.get(cpf=cpf)
            name = patient.name
            cpf = patient.cpf
            return {"name": name, "cpf": cpf}
        except Patient.DoesNotExist:
            return (404, {"message": "Paciente não encontrado"})


api.register_controllers(
    PatientController

)
