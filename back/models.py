from sqlmodel import SQLModel, Field
from sqlalchemy import create_engine
from sqlmodel import Session, select
from typing import Optional

engine = create_engine("sqlite:///database.db")

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Add sample connections if table is empty
        if not session.exec(select(DBConnection)).first():
            session.add_all([
                DBConnection(name="PostgreSQL Main", connection_url="postgresql://user:password@host:port/dbname", type="postgresql"),
                DBConnection(name="Local SQLite", connection_url="sqlite:///path/to/database.db", type="sqlite"),
            ])
            session.commit()

class DBConnection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    connection_url: str
    type: str
