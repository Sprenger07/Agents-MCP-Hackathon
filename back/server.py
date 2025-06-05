from fastmcp import FastMCP
from typing import List, Dict
from sqlmodel import SQLModel, Session, select, create_engine
from models import DBConnection
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

mcp = FastMCP(name="MyRemoteServer")

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

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name} is dep trai!"

@mcp.tool()
def get_connections() -> List[Dict]:
    """
    Return a list of available DB connections on the server from the DBConnection table.
    """
    with Session(engine) as session:
        connections = session.exec(select(DBConnection)).all()
        return [
            {
                "id": conn.id,
                "name": conn.name,
                "connectionURL": conn.connection_url,
                "type": conn.type
            } for conn in connections
        ]

@mcp.tool()
def explore_schemas(source: str, query: str) -> List[Dict]:
    """
    Explore schemas of both source and destination databases, return a list of tables and columns.
    For now, this is a mock implementation.
    """
    # TODO: Replace with actual DB query logic
    # Example output structure
    return [
        {
            "table": "users",
            "columns": ["id", "name", "email"]
        },
        {
            "table": "orders",
            "columns": ["id", "user_id", "amount"]
        }
    ]

if __name__ == "__main__":
    # Initialize database and tables
    init_db()
    # Run with HTTP transport for remote access
    mcp.run()
