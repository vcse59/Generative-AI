from .server import serve

def main():
    import asyncio
    print("This is the MCP Server package. It is not meant to be run directly.")
    asyncio.run(serve())
if __name__ == "__main__":
    main()