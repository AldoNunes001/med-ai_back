
from typing import Any
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import HttpBearer, HttpBasicAuth
import jwt
from .schema import UserSchema, UserResponseSchema, NotAuthenticatedError

api = NinjaAPI()

JWT_SECRET = "diogofredoferreira"
MY_TOKEN = ""


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
        if token == MY_TOKEN:
            return token
        return token
    

@api.get("/get_patient/{cpf}", auth=AuthBearer())
def home(request):
    print("request", request.auth)
    return {"name": "Hello, world!", "cpf": "12345678901"}



def generate_jwt(user):
    token = jwt.encode({"username": user.username}, JWT_SECRET, algorithm="HS256")
    return token


# class BasicAuth(HttpBasicAuth):
#     def authenticate(self, request, username, password):
#         # print(username, password)
#         # user = auth_authenticate(request, username=username, password=password)            
#         # if user is not None:
#         #     auth_login(request, user)
#         #     token = generate_jwt(user)
#         #     return (username, token)
#         if username == "harry" and password == "teste1234":
#             return "oal"

# @api.post("/login", auth=BasicAuth())
# def teste(request):
#     # user = authenticate(request, username=data.username, password=data.password)
#     # if user is not None:
#     #     login(request, user)
#     #     token = generate_jwt(user)
#         # return {"username": user.username, "token": token}
#     # if request.
#     username, token = request.auth
#     # print(username, token)
#     # if username is not None and token is not None:
#     #     username
#     #     return {"username": reques, "token": token}
#     # print("request", request.auth)
#     # print(type(request.auth))
#     MY_TOKEN = token
#     request.session[MY_TOKEN] = token
#     print(request.session[MY_TOKEN])
#     return {"username": username, "token": token}


@api.post("/login", response={200: UserResponseSchema, 403: NotAuthenticatedError})
def teste(request, data: UserSchema):
    user = auth_authenticate(request, username=data.username, password=data.password)
    # print(user)
    # print(request)
    if user is not None:
        auth_login(request, user)
        token = generate_jwt(user)
        global MY_TOKEN
        MY_TOKEN = token
        # request.session["MY_TOKEN"] = token
        # print(request.session["MY_TOKEN"])
        return {"username": user.username, "token": token}
    return (403, {"message": "Usuário ou senha inválidos"})


# @api.post("/teste", response={200: UserResponseSchema, 403: NotAuthenticatedError})
# def teste(request, data: UserSchema):
#     user = auth_authenticate(request, username=data.username, password=data.password)
#     if user is not None:
#         auth_login(request, user)
#         return {"username": user.username, "is_authenticated": True}
#     return (403, {"message": "Usuário ou senha inválidos"})
