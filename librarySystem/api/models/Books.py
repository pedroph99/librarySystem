import datetime
from pydantic import BaseModel, model_validator, Field
from typing import Optional, List, Dict

class Book(BaseModel):
    title: str
    author: str
    copies: int 
    
    # Deixamos o campo opcional para que o validador possa preenchê-lo
    avaliable_copies: Optional[int] = None
    
    genre: Optional[str] = None
    
    # Corrigido: o padrão para uma lista deve ser uma lista vazia
    reserves: List[Dict] = Field(default_factory=list)

    @model_validator(mode='before')
    @classmethod
    def set_available_copies_if_none(cls, data: Dict) -> Dict:
        """
        Se 'avaliable_copies' não for fornecido na criação do modelo,
        define seu valor para ser igual a 'copies'.
        """
        # Verifica se 'avaliable_copies' não foi passado ou é None
        if data.get('avaliable_copies') is None:
            # Pega o valor de 'copies' do dicionário de dados de entrada
            copies_value = data.get('copies')
            if copies_value is not None:
                data['avaliable_copies'] = copies_value
        
        return data



class Reserve(BaseModel):
    user_id: str
    date_reserved: datetime.datetime = datetime.datetime.now()
    date_expires: datetime.datetime = None


    @model_validator(mode='before')
    @classmethod
    def set_date_expires_if_none(cls, data: Dict):
        """
        Se 'date_expires' não for fornecido na criação do modelo,
        define seu valor para ser igual a 'date_reserved'.
        """
        # Verifica se 'date_expires' não foi passado ou é None
        if data.get('date_expires') is None:
            # Pega o valor de 'date_reserved' do dicionário de dados de entrada
            date_reserved_value = data.get('date_reserved')
            if date_reserved_value is not None:
                data['date_expires'] = date_reserved_value.date() + datetime.timedelta(days=15)
            return
        else:
            # Verifica a data de expiração. Se menor que agora, é totalmente invalido
            date_expires_value = data.get('date_expires')
            if date_expires_value is not None:
                if date_expires_value < datetime.datetime.now():
                    raise ValueError('Data de expiração inválida')
            
            return 


# Exceções relacionadas aos livros
class BookNotFoundException(Exception):
    """
    Chamada após o livro não ser encontrado.
    """
    def __init__(self, message = "Livro não encontrado."):
        self.message = message

class BookNotAvailableException(Exception):
    """
    Chamada após o livro não estar disponível.
    """
    def __init__(self, message = "Livro não está disponível."):
        self.message = message
    

class BookReservedException(Exception):
    """
    Chamada após o livro estar reservado.
    """
    def __init__(self, message = "Livro já reservado por este usuário"):
        self.message = message

class BookNotReservedException(Exception):
    """
    Chamada após o livro não estar reservado.
    """
    def __init__(self, message = "Livro não reservado por este usuário"):
        self.message = message