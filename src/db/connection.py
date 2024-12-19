from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL="mysql+pymysql://root:sklookie@127.0.0.1:3307/unify_chat"
engine=create_engine(DATABASE_URL, echo=True)
SessionFactory=sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session=SessionFactory()
    try:
        yield session
    finally:
        session.close()