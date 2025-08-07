import datetime
from fastapi.responses import JSONResponse
from bson import ObjectId
import motor

from librarySystem.api.models.Books import Book, BookNotAvailableException, BookNotFoundException, BookNotReservedException, BookReservedException, Reserve


async def get_books_control(database, params: dict):
    """
    Realiza uma consulta no banco de dados de usuários.

    @param database: objeto do motor que representa o banco de dados.
    @param params: dicionário contendo os campos a serem filtrados.
    @return: lista de usuários filtrados.
    
    O body: dict é colocado de maneira proposital para uma consulta mais dinâmica, sendo possível filtrar os campos de acordo com o que for desejado.
    Exemplo:
    {
        "name": "pedro",
        "age": 25
    }
    PARAM 1 ILIKE "$1" AND PARAM 2 ILIKE "$2" AND ....
    """
    query = {

    }
    print(query)
    for x in params:
        #Damos prioridade ao id. Se o id for passado, ele será usado para filtrar o livro, e exclusivamente ele.
        if x == "id" or x == "_id":
            query = {"_id": ObjectId(params[x])}
            break
        query[x] = {"$regex": f"{params[x]}", "$options": "i"  }
    
    books_db = await database.db['books'].find(query).to_list(length=100)
    print(books_db)
    for book in books_db:
        book['_id'] = str(book['_id'])
    
    return books_db

async def insert_book_control(database, book: list[Book]):
    """
    Insere um usuário no banco de dados.

    @param database: objeto do motor que representa o banco de dados.
    @param books: Lista de livros que serão inseridos no banco de dados.
    """
    if len(book) == 0:
        raise Exception("Nenhum livro foi inserido.")
    
    books = _books_to_dict(book)
    print(f" Os livros são: {books}")
    
    # Insere os livros no banco de dados
    try:
        await database.db['books'].insert_many(books)

    except Exception as e:
        raise Exception(f"Erro ao inserir livro(s): {e}")

    
    return books
    
async def reserve_book_control(database, book_id: str, user_id: str, date_expires: datetime.datetime = None):
    """
    Reserva um livro no banco de dados.

    @param database: objeto do motor que representa o banco de dados.
    @param book_id: id do livro que será reservado.
    """
    # Busca o livro por ID. Caso não encontre, raise Exception
    book = await get_books_control(database= database, params={"_id": book_id})
    print(f"Livro: {book}")
    if len(book) == 0:
        raise BookNotFoundException("Livro não encontrado.")
    selected_book = book[0]

    # Verifica se o livro está disponível
    if selected_book['avaliable_copies'] <= 0:
        raise BookNotAvailableException(f"Livro {selected_book['title']} não está disponível.")
    
    # Verifica se o usuário já está reservando o livro
    if selected_book['reserves']:
        for reserve in selected_book['reserves']:
            if reserve['user_id'] == user_id:
                raise BookReservedException("O usuário já está reservando este livro.")
    

    #Validação do modelo de reserva
    dict_to_reserve = {
        "user_id": user_id,
        "date_reserved": datetime.datetime.now(),
        "date_expires": date_expires.strftime("%Y-%m-%d") if date_expires is not None else (datetime.datetime.now().date() + datetime.timedelta(days=15)).strftime("%Y-%m-%d")
    }
    #_validate_reserve(dict_to_reserve)

    # Insere a reserva no banco de dados, além de diminuir o número de cópias disponíveis
    try:
        await database.db['books'].update_one(
    {"_id": ObjectId(book_id)},  # 1. Filtro
    {                            # 2. Documento de atualização com AMBOS operadores
        "$inc": {"avaliable_copies": -1},
        "$push": {"reserves": dict_to_reserve}
    }
)


        return True
    except Exception as e:
        raise Exception(f"Erro ao reservar livro: {e}")
    
    

    # Começa a lógica de reservar o livro
    
def _books_to_dict(books: list[Book]):
    """
    Função auxiliar que transforma uma lista de Book em uma lista de dicionários.
    """
    return [book.dict() for book in books]

def _validate_reserve(reserve: dict):
        """
        Valida uma reserva de acordo com um conjunto de regras.
        Levanta Exception se alguma regra for violada.
        """
        # Regra 1: Data de reserva não pode ser maior que a data de expiração
        Reserve(user_id=reserve['user_id'], date_reserved=reserve['date_reserved'], date_expires=reserve['date_expires'])


async def reedem_book_control(database, book_id: str, user_id: str):
    """
    Devolve o livro à biblioteca.

    @param database: objeto do motor que representa o banco de dados.
    @param book_id: id do livro que será devolvido.
    """
    # Busca o livro por ID. Caso não encontre, raise Exception
    book = await get_books_control(database= database, params={"_id": book_id})
    print(f"Livro: {book}")
    if len(book) == 0:
        raise BookNotFoundException("Livro não encontrado.")
    selected_book = book[0]

    # Verifica se o livro está reservado
    if not selected_book['reserves']:
        raise BookNotReservedException(f"Livro não reservado pelo usuário {user_id}.")
    
    # Verifica se o usuário já está reservando o livro
    for reserve in selected_book['reserves']:
        if reserve['user_id'] == user_id:
            await database.db['books'].update_one({"_id": ObjectId(book_id)},
                                                  {"$inc": {"avaliable_copies": 1},
                                                   "$pull": {"reserves": 
                                                             {"user_id": user_id}
                                                             }
                                                   })
            return True
    
    raise BookNotReservedException(f"Livro não reservado pelo usuário {user_id}.")
