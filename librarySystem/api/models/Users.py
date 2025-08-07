
from pydantic import BaseModel


class User(BaseModel):
    """
    Classe base para o usuário
    """
    username: str
    password: str
    email: str
    active: bool

class UserCredentials(BaseModel):
    """
    credenciais do usuário -> Password e username
    """
    username: str
    password: str

#Exceções relacionadas a operações de usuário.
class passwordException(Exception):

    def __init__(self, message):
        self.message = message

class FilterNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

class BadCredentialsException(Exception):
    def __init__(self, message):
        self.message = message