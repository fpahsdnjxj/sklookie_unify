import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
SessionFactory=sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session=SessionFactory()
    try:
        yield session
    finally:
        session.close()
