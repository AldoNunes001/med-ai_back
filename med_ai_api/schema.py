from ninja import Schema


class UserSchema(Schema):
    username: str
    password: str


class UserResponseSchema(Schema):
    username: str
    token: str


class PatientResponseSchema(Schema):
    name: str
    cpf: str
    

class PatientAddSchema(Schema):
    name: str
    cpf: str
    username: str

class NotAuthenticatedError(Schema):
    message: str
    is_authenticated: bool = False

    
class NotFoundError(Schema):
    message: str
    is_found: bool = False
