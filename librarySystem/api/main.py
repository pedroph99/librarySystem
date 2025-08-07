from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from librarySystem.api.control.jwtControllers import create_access_token
from librarySystem.api.control.userControllers import login_user_control
from librarySystem.api.models.DatabaseConnection.connection import DatabaseConnection
from librarySystem.api.models.Users import BadCredentialsException, UserCredentials
from librarySystem.api.views.UserRoutes import router as UserRoutes
from librarySystem.api.views.BookRoutes import router as BookRoutes
from librarySystem.tools.credentials import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
# CREATE AN MAIN FASTAPI APP
# USE make dev or make prod on command line to run the fastapi server
#

# Cria um lifespan para o app, gerando uma interface global para o banco de dados e outras coisas necessárias para o app funcionar
#De certa forma, prepara-se o app para rodar, realizando uma checagem antes de iniciar o app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Connecting to database...')
    database = DatabaseConnection()
    await database.connect_client()
    print('Client connected!')
    await database.connect_db()
    print('Database connected!')

    app.state.db = database

    yield

    await database.client.close()
app = FastAPI(lifespan=lifespan)

# Adiciona rotas ao app
app.include_router(BookRoutes, prefix="/books", tags=["Books"])
app.include_router(UserRoutes, prefix="/users", tags=["Users"])
# Adiciona rotas para o Swagger
@app.middleware("http")
async def validate_user(request: Request, call_next):
  """
  Middleware responsável por verificar a autenticação do usuário em chamadas gerais para a API.
  Por motivos óbvios, precisamos desviar a validação na rota de login.
  @param request: objeto Request do FastAPI.
  @param call_next: função que chama o próximo middleware ou a rota final.

  O token deve ser passado no header Authorization como o seguinte:
  Authorization: Bearer <token JWT>
  """
  if not request.url.path.startswith("/login"):

    token = request.headers.get("Authorization")
    if not token: 
        return JSONResponse(status_code=401, content={"message": "Token não encontrado"})
    token = token.replace("Bearer ", "").strip()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            

            request.state.user = payload
            return await call_next(request)
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, 
                                content={"message": "Token expirado"})
        except JWTError:
            return JSONResponse(status_code=401, 
                                content={"message": "Erro de token"})
        except Exception as e:
            return JSONResponse(status_code=500, 
                                content={"message": f"Erro: {e}"})
    

  return await call_next(request)


@app.post("/login")
async def login(request: Request, body: UserCredentials):
    """
    Verifica as credenciais no banco de dados e gera um token de acesso. O token tem validade de uma hora, por degault. 
    @param request: objeto Request do FastAPI.
    @param body: objeto UserCredentials do FastAPI.
    """
    database = request.app.state.db
    try:
        user_db = await login_user_control(database= database, user=body)
        
        jwt_credentials = {"username": user_db['username'], "password": user_db['password'], "user_id": str(user_db['_id']).replace("ObjectId(", "").replace(")", "")}
        token = create_access_token(data=jwt_credentials)
        return JSONResponse(status_code=200, content={"message": "Login bem sucedido", "token": token})
    except BadCredentialsException as e:
        return JSONResponse(status_code=400, content={"message": f"Erro ao logar: {e.message}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Erro ao logar: {e}"})