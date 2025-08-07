import os
from dotenv import load_dotenv

#Carrega o dotenv...
#O strip irá tirar os espaços em branco no inicio e no final da string, caso houver
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL").strip()
DB_NAME = os.getenv("DB_NAME").strip()
SECRET_KEY = os.getenv("SECRET_KEY").strip()
ALGORITHM = os.getenv("ALGORITHM").strip()