import asyncio
from connection import Server

if __name__ == "__main__":
    server = Server()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Остановка сервера...")
