from .client import handle_input

def main():
    import asyncio
    user_input = input("Enter your query: ")
    if not user_input.strip():
        print("❌ No input provided. Exiting.")
        return
    asyncio.run(handle_input(user_input))