import datetime
from jose import jwt, JWTError

from librarySystem.tools.credentials import ALGORITHM, SECRET_KEY

def create_access_token(data: dict, expires_delta: int = 3600):
    """
    
    Criação de um token de acesso JWT com duração por default de 1 hora.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_delta)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    data = {"username": "pedro", "password": "123456"}
    token = create_access_token(data)
    print(token)
