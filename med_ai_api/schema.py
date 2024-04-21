from ninja import Schema


class UserSchema(Schema):
    username: str
    password: str


class UserResponseSchema(Schema):
    username: str
    token: str


class NotAuthenticatedError(Schema):
    message: str
    is_authenticated: bool = False
