from fastmcp import FastMCP

mcp = FastMCP(name="MyRemoteServer")

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Run with HTTP transport for remote access
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
