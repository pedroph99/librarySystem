import traceback
from fastapi import FastAPI, APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from librarySystem.api.control.userControllers import get_user_control, insert_user_control, update_user_control
from librarySystem.api.models.Users import FilterNotFoundException, User, passwordException

import pymongo.errors as pymongo_exceptions
router = APIRouter()

@router.get("/")
async def get_users(request: Request, body: dict = None):
    """
    Realiza uma consulta no banco de dados de usuários.
    @param body: dicionário contendo os campos a serem filtrados.
    @return: lista de usuários filtrados.
    
    O body: dict é colocado de maneira proposital para uma consulta mais dinâmica, sendo possível filtrar os campos de acordo com o que for desejado.
    Exemplo:
    {
        "name": "pedro",
        "age": 25
    }
    Filtrará usuários por nome e idade, enquanto {} fará uma busca geral. A busca é feita como se fosse um ILIKE no SQL.
    """
    database = request.app.state.db

    users_db = await get_user_control(database= database, params=body)
    
    
    return JSONResponse(status_code=200, content=jsonable_encoder(users_db))


@router.post("/")
async def insert_user(request: Request, body: list[User]):
    """
    Insere um usuário ou mais no banco de dados
    """


    database = request.app.state.db


    try:
        user_db = await insert_user_control(database= database, users=body)
    
    
    except pymongo_exceptions.DuplicateKeyError as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Erro ao inserir usuário(s): Nome de usuário já existente"})
    
    except passwordException as e:
        return JSONResponse(status_code=400, content={"message": f"Erro ao inserir usuário(s): {e.message}"})

    
    except pymongo_exceptions.BulkWriteError as e:
        return JSONResponse(status_code=400, content={"message": f"Erro ao inserir usuário(s): Username duplicado {e}"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Erro ao inserir usuário(s): {e}"})


    return JSONResponse(status_code=200, content={
        "message": f"Usuário(s)  inserido(s) com sucesso.",
        
    })
    
    print(f"resposta do userControllers: {user_db.status_code}")



@router.put("/")
async def update_user(request: Request, body: list[dict]):
    """
    Atualiza um usuário no banco de dados.
    """
    database = request.app.state.db
    try:
        user_db = await update_user_control(database = database, user_info = body)

        return JSONResponse(status_code=200, content={"message": f"Usuário(s)  atualizado(s) com sucesso."})
    
    except FilterNotFoundException as e:
        return JSONResponse(status_code=400, content={"message": f"Não foram encontrados os campos username ou id em algum usuário: {e.message}"})

    except passwordException as e:
        return JSONResponse(status_code=400, content={"message": f"Erro ao atualizar  a senha de algum usuário(s): {e.message}"})

    except Exception as e:
        return JSONResponse(status_code=200, content={"message": f"Erroa ao atualizar usuário(s): {e}"})
