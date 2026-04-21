import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener la URL de conexión desde el archivo .env o usar una por defecto para desarrollo
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin_user:password_seguro_db@app-db:5432/app_main_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión de base de datos en las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
