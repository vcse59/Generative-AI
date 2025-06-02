from mcp.server.fastmcp import FastMCP

# Main asynchronous function to start the MCP server
async def serve():

    # Initialize the FastMCP server with configuration
    server_mcp = FastMCP(
        "This is the MCP Server with basic arithmetic tools",
        version="1.0.0",
        host="0.0.0.0",
        port=8080,
        stateless_http=True,
        json_response=True
    )

    # Tool: Add two numbers
    @server_mcp.tool(description="Adds two numbers", name="addition")
    def addition(a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b

    # Tool: Subtract two numbers
    @server_mcp.tool(description="Subtract two numbers", name="subtraction")
    def subtraction(a: int, b: int) -> int:
        """Subtract two numbers."""
        return a - b
    
    # Tool: Multiply two numbers
    @server_mcp.tool(description="Multiply two numbers", name="multiplication")
    def multiplication(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    # Tool: Divide two numbers, with zero division check
    @server_mcp.tool(description="Divide two numbers", name="division")
    def division(a: int, b: int) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    # Start the server with streamable HTTP support
    await server_mcp.run_streamable_http_async()