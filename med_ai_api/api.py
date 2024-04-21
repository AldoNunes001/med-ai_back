from typing import Any
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import Patient
from ninja import NinjaAPI
from ninja.security import HttpBearer, HttpBasicAuth
import jwt
from .schema import UserSchema, UserResponseSchema, NotAuthenticatedError

api = NinjaAPI()

JWT_SECRET = "diogofredoferreira"


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        
        # payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = payload.get("username")
        
        user = str(User.objects.get(username=username))
        if username == user:
            return token
        

@api.get("/get_patient/{cpf}", auth=AuthBearer())
def get_patient(request, cpf):

    try:
        patient = Patient.objects.get(cpf=cpf)
        name = patient.name
        cpf = patient.cpf
        return {"name": name, "cpf": cpf}
    except Patient.DoesNotExist:
        return (404, {"message": "Paciente não encontrado"})


def generate_jwt(user):
    token = jwt.encode({"username": user.username}, JWT_SECRET, algorithm="HS256")
    return token


@api.post("/login", response={200: UserResponseSchema, 403: NotAuthenticatedError})
def login(request, data: UserSchema):
    user = auth_authenticate(request, username=data.username, password=data.password)
    if user is not None:
        auth_login(request, user)
        token = generate_jwt(user)
        global MY_TOKEN
        MY_TOKEN = token
        return {"username": user.username, "token": token}
    return (403, {"message": "Usuário ou senha inválidos"})
