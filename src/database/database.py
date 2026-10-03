
from sqlmodel import Session, create_engine

url = "sqlite:///db_turnos_sqlmodel.db"

engine = create_engine(url, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session
