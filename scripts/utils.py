import os
from sqlalchemy import create_engine

def get_db_connection():
    # Toma la URL de Docker si existe; de lo contrario usa localhost:5433 para tu terminal de Fedora
    default_url = "postgresql+psycopg2://saul:supersecreto@127.0.0.1:5433/postgres"
    db_url = os.getenv("DB_URL", default_url)
    
    print(f"-> Conectando a la base de datos usando: {db_url}")
    engine = create_engine(db_url)
    return engine