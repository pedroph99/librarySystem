
import traceback
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from librarySystem.api.control.bookControllers import get_books_control, insert_book_control, reedem_book_control, reserve_book_control
from librarySystem.api.models.Books import Book, BookNotFoundException, BookNotReservedException, BookReservedException

import motor.motor_asyncio

router = APIRouter()

@router.get("/")
async def get_books(request: Request, body: dict = None):
    db = request.app.state.db
    
    books = await get_books_control(database= db, params=body)

    return JSONResponse(status_code=200, content=jsonable_encoder(books))
@router.post("/")
async def insert_book(request: Request, body: list[Book]):
    """
    Insere um usuário no banco de dados.
    """

    database = request.app.state.db
    try:
        book_db = await insert_book_control(database= database, book=body)

        string_book = ""
        for book in book_db:
            string_book += f"{book['title']} "
        return JSONResponse(status_code=200, content={"message": f"Livro(s) {string_book} inserido(s) com sucesso."})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Erro ao inserir livro(s): {e}"})


@router.post("/reserve/{book_id}")
async def reserve_book(request: Request, book_id: str, expires_days: int = None):
    """
    Reserva um livro no banco de dados. É preciso verificar a quantidade de livros disponíveis
    além de verificar se o usuário já possui um livro reservado daquele título.
    """
    database = request.app.state.db
    user_info = request.state.user
    user_id = user_info['user_id']
    try:
        await reserve_book_control(database= database, book_id= book_id, user_id= user_id)

        return JSONResponse(status_code=200, content={"message": f"Livro reservado com sucesso."})
    except BookNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": f"Livro não encontrado"})
    except BookReservedException as e:
        return JSONResponse(status_code=400, content={"message": f"Livro já reservado"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Erro desconhecido"})

@router.post("/redeem/{book_id}")
async def redeem_book(request: Request, book_id: str):
    """
    Função para fazer o reverso de reservar: devolver o livro à biblioteca.
    """

    database = request.app.state.db
    user_info =  request.state.user
    user_id = user_info['user_id']
    try:
        await reedem_book_control(database= database, book_id= book_id, user_id= user_id)
        return JSONResponse(status_code=200, content={"message": f"Livro devolvido com sucesso."})
    except BookNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": f"Livro não encontrado"})
    except BookNotReservedException as e:
        return JSONResponse(status_code=400, content={"message": f"Livro não reservado"})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"erro desconhecido"}) 


    