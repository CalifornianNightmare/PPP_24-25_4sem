import asyncio
import sys
from protocol import Protocol
from config import SERVER_HOST, SERVER_PORT, DELIMITER

class Client:
    """
    Асинхронный TCP клиент, отправляющий команды серверу и получающий ответы.
    """

    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port

    async def send_command(self, command):
        """
        Устанавливает соединение с сервером, отправляет команду и получает ответ.
        """
        reader, writer = await asyncio.open_connection(self.host, self.port)

        await Protocol.send_message(writer, command)
        response = await Protocol.recv_message(reader)
        print(self.format_response(response))

        writer.close()
        await writer.wait_closed()

    def format_response(self, response):
        """
        Форматирует ответ сервера для удобного вывода.
        """
        if response.startswith("list "):
            apps = response[len("list "):]
            return f"Доступные программы:\n{apps}"
        elif response.startswith("message "):
            return response[len("message "):]
        return response

    def run(self):
        """
        Запускает клиент в режиме командной строки.
        """
        if len(sys.argv) < 2:
            print("Использование: python client.py <команда>")
            return
        
        command = DELIMITER.join(sys.argv[1:])
        asyncio.run(self.send_command(command))

