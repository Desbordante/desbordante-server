from typing import TypedDict


class RegisterUserData(TypedDict):
    email: str
    password: str
    full_name: str
    country: str
    company: str
    occupation: str


class LoginUserData(TypedDict):
    email: str
    password: str


class RegisteredUser(TypedDict):
    id: int
    email: str
    full_name: str
    country: str
    company: str
    occupation: str


class RegisteredUserResponse(TypedDict):
    user: RegisteredUser
    access_token: str
    refresh_token: str
