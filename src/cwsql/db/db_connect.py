from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

load_dotenv()

def connect_to_db(dbname='bcu', set_autocommit=False):
    dbname = dbname or os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PWD')
    host = os.getenv('DB_HOST')

    # Tentative de connexion à la base de données
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        if set_autocommit:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"Connexion à la base de données {dbname} réussie.")
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données {dbname}: {e}")
        exit(1)  # Quitte le script en cas d'échec de la connexion
