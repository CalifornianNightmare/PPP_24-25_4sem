import asyncio
import json
from protocol import Protocol
from app_manager import AppManager
from config import SERVER_HOST, SERVER_PORT, DELIMITER


class Server:
    """
    Асинхронный TCP сервер, принимающий команды от клиентов и управляющий программами.
    """

    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.app_manager = AppManager()
        self.server = None

    async def handle_client(self, reader, writer):
        """
        Обрабатывает подключения клиентов. Получает и выполняет команды.
        """
        addr = writer.get_extra_info('peername')
        print(f"Подключен клиент {addr}")

        try:
            while True:
                data = await Protocol.recv_message(reader)
                if not data:
                    break

                response = await self.process_command(data)
                await Protocol.send_message(writer, response)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            print(f"Отключение клиента {addr}")
            writer.close()
            await writer.wait_closed()

    async def process_command(self, command):
        """
        Обрабатывает команды от клиента и вызывает соответствующие методы.
        """
        parts = command.split(DELIMITER)
        cmd = parts[0]

        if cmd == "add":
            if len(parts) < 6:
                return "message Ошибка: не хватает аргументов"
            return await self.app_manager.add_app(*parts[1:])

        elif cmd == "remove":
            if len(parts) < 2:
                return "message Ошибка: не хватает аргументов"
            return await self.app_manager.remove_app(parts[1])

        elif cmd == "start":
            return await self.app_manager.start_app(parts[1])

        elif cmd == "stop":
            return await self.app_manager.stop_app(parts[1])

        elif cmd == "applist":
            return f"list {json.dumps(await self.app_manager.list_apps())}"

        elif cmd == "get":
            return await self.app_manager.get_app_result(parts[1])

        elif cmd == "shutdown":
            await self.shutdown()
            return "message Сервер выключается"

        else:
            return "message Неизвестная команда"

    async def shutdown(self):
        """
        Завершает работу сервера.
        """
        print("Выключение сервера...")
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def start(self):
        """
        Запускает сервер и принимает подключения.
        """
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Сервер запущен на {self.host}:{self.port}")

        async with self.server:
            await self.server.serve_forever()


