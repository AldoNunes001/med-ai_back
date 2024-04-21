
from typing import Any
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import HttpBearer
import jwt
from .schema import UserSchema, UserResponseSchema, NotAuthenticatedError

api = NinjaAPI()

JWT_SECRET = "diogofredoferreira"


# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         try:
#             payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#             username = payload.get("username")
#             user = authenticate(request, username=username)
#             if user is not None:
#                 return user
#         except jwt.PyJWTError:
#             return None

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        return token
    

@api.get("/get_patient/{cpf}", auth=AuthBearer())
def home(request):
    print("request", request.auth)
    return {"name": "Hello, world!", "cpf": "12345678901"}



def generate_jwt(user):
    token = jwt.encode({"username": user.username}, JWT_SECRET, algorithm="HS256")
    return token


@api.post("/login", response={200: UserResponseSchema, 403: NotAuthenticatedError})
def teste(request, data: UserSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        token = generate_jwt(user)
        return {"username": user.username, "token": token}
    return (403, {"message": "Usuário ou senha inválidos"})


# @api.post("/teste", response={200: UserResponseSchema, 403: NotAuthenticatedError})
# def teste(request, data: UserSchema):
#     user = authenticate(request, username=data.username, password=data.password)
#     if user is not None:
#         login(request, user)
#         return {"username": user.username, "is_authenticated": True}
#     return (403, {"message": "Usuário ou senha inválidos"})
