from models import Connection, engine
from sqlmodel import Session
from sqlalchemy import create_engine, inspect
from sqlmodel import select
from dataclasses import dataclass
import sqlparse
from sqlalchemy import text


@dataclass
class Column:
    name: str
    type: str


@dataclass
class Schema:
    table: str
    columns: list[Column]


class CommentService:
    @staticmethod
    def list_table(connection_id: int):
        """
        Return a list of all table names for the given connection.
        """
        # Get connection_url from Connection table
        with Session(engine) as session:
            conn = session.exec(
                select(Connection).where(Connection.id == connection_id)
            ).first()
            if not conn:
                raise ValueError(f"Connection id {connection_id} not found")
            target_engine = create_engine(conn.connection_url)
            inspector = inspect(target_engine)
            return inspector.get_table_names()

    @staticmethod
    def get_table_schemas(connection_id: int) -> list[Schema]:
        with Session(engine) as session:
            conn = session.exec(
                select(Connection).where(Connection.id == connection_id)
            ).first()
            if not conn:
                raise ValueError(f"Connection id {connection_id} not found")
            target_engine = create_engine(conn.connection_url)
            inspector = inspect(target_engine)
            tables = inspector.get_table_names()
            schemas = []
            for table in tables:
                columns = [
                    Column(name=col["name"], type=str(col["type"]))
                    for col in inspector.get_columns(table)
                ]
                schemas.append(Schema(table=table, columns=columns))
            return schemas

    @staticmethod
    def get_table_schema(connection_id: int, table_name: str) -> Schema:
        with Session(engine) as session:
            conn = session.exec(
                select(Connection).where(Connection.id == connection_id)
            ).first()
            if not conn:
                raise ValueError(f"Connection id {connection_id} not found")
            target_engine = create_engine(conn.connection_url)
            inspector = inspect(target_engine)
            if table_name not in inspector.get_table_names():
                raise ValueError(
                    f"Table '{table_name}' not found in connection {connection_id}"
                )
            columns = [
                Column(name=col["name"], type=str(col["type"]))
                for col in inspector.get_columns(table_name)
            ]
            return Schema(table=table_name, columns=columns)

    @staticmethod
    def read(connection_id: int, query: str) -> list[dict] :
        parsed = sqlparse.parse(query)
        if not parsed or parsed[0].get_type() != "SELECT":
            raise ValueError("Only SELECT (readonly) queries are allowed.")

        with Session(engine) as session:
            conn = session.exec(
                select(Connection).where(Connection.id == connection_id)
            ).first()
            if not conn:
                raise ValueError(f"Connection id {connection_id} not found")
            target_engine = create_engine(conn.connection_url)
            with target_engine.connect() as connection:
                result = connection.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()
                # Return as list of dicts
                return [dict(zip(columns, row)) for row in rows]
