from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///instance/test.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class Base(DeclarativeBase):
    pass

def init_db():
    Base.metadata.create_all(bind=engine)