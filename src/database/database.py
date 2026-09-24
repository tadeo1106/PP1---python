from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

url = f"sqlite:///db_turnos_sqlmodel.db"

engine = create_engine(url, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session
