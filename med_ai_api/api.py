
from django.contrib.auth import authenticate, login
from ninja import NinjaAPI
from ninja.security import django_auth
from .schema import UserSchema, UserResponseSchema, NotAuthenticatedError

api = NinjaAPI()


@api.get("/get_patient/{cpf}", auth=django_auth)
def home(request):
    print("request", request.auth)
    return {"name": "Hello, world!", "cpf": "12345678901"}





@api.post("/teste", response={200: UserResponseSchema, 403: NotAuthenticatedError})
def teste(request, data: UserSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        login(request, user)
        return {"username": user.username, "is_authenticated": True}
    return (403, {"message": "Usuário ou senha inválidos"})
