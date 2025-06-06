# MCP Tool: list_table

**Description:**
Returns a list of all table names for the given database connection.

**Parameters:**
- `connection_id` (int): The ID of the database connection to inspect.

**Returns:**
- `list[str]`: A list of table names in the connected database.

**Example Usage:**
list_table(connection_id=1)
# Output: [
#   "employee",
#   "department",
#   ...
# ]

**Notes:**
- Use `get_connections` to find valid connection IDs.
- Don't use this tool without having a valid connection ID.