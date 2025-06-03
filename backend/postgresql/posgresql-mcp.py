from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
import os

mcp = FastMCP("postgresql-mcp")


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

@mcp.tool()
async def execute_query(query : str) -> int:
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = [dict(row._mapping) for row in result]
            return rows
    except Exception as e:
        return [f"Erreur : {str(e)}"]


if __name__ == "__main__":
    mcp.run()
