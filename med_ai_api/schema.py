from ninja import Schema


class PatientResponseSchema(Schema):
    name: str
    cpf: str


class PatientAddSchema(Schema):
    name: str
    cpf: str
    username: str


class NotFoundError(Schema):
    message: str
    is_found: bool = False
