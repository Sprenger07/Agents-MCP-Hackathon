from fastmcp import FastMCP
from sqlmodel import Session, select
from models import Connection, engine
from services.connection import ConnectionService, Schema
import os
#TODO: make read-only endpoints resource instead of tool

mcp = FastMCP(name="MyRemoteServer")


def read_prompt_md(filename):
    path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name} dep trai!"

@mcp.tool(description=read_prompt_md("get_connections.md"))
def get_connections():
    with Session(engine) as session:
        connections = session.exec(select(Connection)).all()
        return list(connections)

@mcp.tool(description=read_prompt_md("list_table.md"))
def list_table(connection_id: int) -> list[str]:
    return ConnectionService.list_table(connection_id)

@mcp.tool(description=read_prompt_md("get_table_schemas.md"))
def get_table_schemas(connection_id: int) -> list[Schema]:
    return ConnectionService.get_table_schemas(connection_id)

@mcp.tool(description=read_prompt_md("get_table_schema.md"))
def get_table_schema(connection_id: int, table_name: str) -> Schema:
    return ConnectionService.get_table_schema(connection_id, table_name)

@mcp.tool(description=read_prompt_md("read.md"))
def read(connection_id: int, query: str) -> list[dict]:
    return ConnectionService.read(connection_id, query)


if __name__ == "__main__":
    mcp.run()
