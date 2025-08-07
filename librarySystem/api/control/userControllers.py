import hashlib
from fastapi.responses import JSONResponse
import motor
from librarySystem.api.models.Users import BadCredentialsException, FilterNotFoundException, User, UserCredentials, passwordException
async def get_user_control(database, params: dict):
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
    for x in params:
        query[x] = {"$regex": f"{params[x]}", "$options": "i"  }
    
    users_db = await database.db['users'].find(query).to_list(length=100)
    for user in users_db:
        user['_id'] = str(user['_id'])
    
    return users_db

async def insert_user_control(database, users: list[dict]):
    """
    Insere um usuário no banco de dados.

    @param database: objeto do motor que representa o banco de dados.
    @param user: objeto User que representa o usuário a ser inserido.
    @return: objeto User que representa o usuário inserido.
    """
    users = _users_to_dict(users)
    print(f"os usuários são: {users}")

    # Valida a senha de cada usuário
    for user in users:
        try:
            _validate_password(user['password'])
            user['password'] = _hash_password(user['password'])
        except passwordException as e:
            
            raise passwordException(f"Erro ao inserir usuário {user['username']}: {e.message}")

    
    user_db = await database.db['users'].insert_many(users)
    return user_db


def _users_to_dict(users: list[User]):
    """
    Função auxiliar que transforma uma lista de User em uma lista de dicionários.
    """
    return [user.dict() for user in users]


def _validate_password(password: str):
    """
    Valida uma senha de acordo com um conjunto de regras.
    Levanta passwordException se alguma regra for violada.
    """
    # Regra 1: Comprimento da senha
    if len(password) < 8 or len(password) > 20:
        raise passwordException("Senha inválida: Deve conter entre 8 e 20 caracteres.")

    # Regra 2: Deve conter pelo menos uma letra maiúscula
    if not any(c.isupper() for c in password):
        raise passwordException("Senha inválida: Deve conter pelo menos uma letra maiúscula.")

    # Regra 3: Deve conter pelo menos um caractere especial
    # Definimos quais caracteres são considerados especiais
    special_characters = "!@#$%^&*()-_=+[]{};:'\",.<>/?|"
    if not any(c in special_characters for c in password):
        raise passwordException(f"Senha inválida: Deve conter pelo menos um caractere especial (ex: {special_characters[0:5]}...).")
        
    # --- Melhorias Adicionais (Recomendado) ---

    # Regra 4: Deve conter pelo menos uma letra minúscula
    if not any(c.islower() for c in password):
        raise passwordException("Senha inválida: Deve conter pelo menos uma letra minúscula.")

    # Regra 5: Deve conter pelo menos um número
    if not any(c.isdigit() for c in password):
        raise passwordException("Senha inválida: Deve conter pelo menos um número.")
    
    return
    
def _hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


async def update_user_control(database, user_info: list[dict]):
    """
    Atualiza um usuário ou vários no banco de dados. Query pode ser feita por username ou id(Prioritário)

    Método:

    [
    {id : ai0oda,
    <info_to_update_1>: <value_to_update_1>,
    <info_to_update_2>: <value_to_update_2>,
    ...
    },
    {
    username : ai0oda,
    <info_to_update_1>: <value_to_update_1>,
    <info_to_update_2>: <value_to_update_2>
    } ...
    
    ]
    """



    for x in user_info:
        query = {
            '$set': {}
        }
        filtro = {}
        # Seta os filtros, dando prioridade ao id
        if 'id' in x:
            filtro['_id'] = x['id']
        
        elif 'username' in x:
            filtro['username'] = x['username']
        else:
            raise FilterNotFoundException("Nenhum filtro encontrado.")
        

        for key, value in x.items():
            if key not in ['id', 'username']:

                if key == 'password':
                    # Valida a senha de cada usuário, caso passada
                    _validate_password(value)
                    value = _hash_password(value)
                
                
                query['$set'][key] = value
        
        print(f"query: {query}")
        print(f"filtro: {filtro}")

        await database.db['users'].update_one(filtro, query)

    return user_info


async def login_user_control(database, user: UserCredentials):
    """
    Realiza uma consulta no banco de dados de usuários.
    
    @param database: objeto do motor que representa o banco de dados.
    @param user: objeto User que representa o usuário a ser inserido.
    @return: objeto User que representa o usuário inserido.
    """
    user_db = await database.db['users'].find_one({"username": user.username})
    if user_db:
        if user_db['password'] == _hash_password(user.password):
            return user_db
    
    #Se a função chegar no final, é chamado uma exceção de credenciais inválidas
    raise BadCredentialsException("Usuário ou senha inválidos.")

