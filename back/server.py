from fastmcp import FastMCP
from sqlmodel import Session, select, create_engine
from models import Connection
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

mcp = FastMCP(name="MyRemoteServer")


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name} is dep trai!"


@mcp.tool()
def get_connections():
    with Session(engine) as session:
        connections = session.exec(select(Connection)).all()
        return list(connections)


# @mcp.tool()
# def explore_schemas(source: str, query: str) -> List[Dict]:
#     return [
#         {"table": "users", "columns": ["id", "name", "email"]},
#         {"table": "orders", "columns": ["id", "user_id", "amount"]},
#     ]


if __name__ == "__main__":
    mcp.run()
