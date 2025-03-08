import asyncio
import os
from connection import Client
from config import DELIMITER, APPS_DIR

REAL_DIR = os.path.dirname(os.path.realpath(__file__))

class ClientMenu:
    """
    Меню для клиента, позволяющее пользователю взаимодействовать с сервером через текстовый интерфейс.
    """

    def __init__(self):
        self.client = Client()

    async def display_menu(self):
        """
        Отображает меню и обрабатывает выбор пользователя.
        """
        while True:
            print("\nМеню:")
            print("1. Добавить программу")
            print("2. Удалить программу")
            print("3. Запустить программу")
            print("4. Остановить программу")
            print("5. Список программ")
            print("6. Получить результат программы")
            print("7. Завершить работу")
            
            choice = input("\nВыберите опцию: ")

            if choice == '1':
                await self.add_program()
            elif choice == '2':
                await self.remove_program()
            elif choice == '3':
                await self.start_program()
            elif choice == '4':
                await self.stop_program()
            elif choice == '5':
                await self.list_programs()
            elif choice == '6':
                await self.get_program_result()
            elif choice == '7':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    async def add_program(self):
        """
        Добавляет новую программу на сервер.
        """
        appname = input("Введите имя программы: ")
        filename = input("Введите имя файла программы: ")
        applaunch = input("Введите команду для запуска программы: ")
        interval = input("Введите интервал в миллисекундах (например, 1000): ")

        filepath = os.path.join(REAL_DIR, APPS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            filecontents = f.read()

        command = f"add{DELIMITER}{appname}{DELIMITER}{filename}{DELIMITER}{applaunch}{DELIMITER}{interval}{DELIMITER}{filecontents}"
        await self.client.send_command(command)

    async def remove_program(self):
        """
        Удаляет программу с сервера.
        """
        appname = input("Введите имя программы для удаления: ")
        command = f"remove{DELIMITER}{appname}"
        await self.client.send_command(command)

    async def start_program(self):
        """
        Запускает программу на сервере.
        """
        appname = input("Введите имя программы для запуска: ")
        command = f"start{DELIMITER}{appname}"
        await self.client.send_command(command)

    async def stop_program(self):
        """
        Останавливает программу на сервере.
        """
        appname = input("Введите имя программы для остановки: ")
        command = f"stop{DELIMITER}{appname}"
        await self.client.send_command(command)

    async def list_programs(self):
        """
        Получает список всех доступных программ.
        """
        command = "applist"
        await self.client.send_command(command)

    async def get_program_result(self):
        """
        Получает результат работы программы.
        """
        appname = input("Введите имя программы для получения результата: ")
        command = f"get{DELIMITER}{appname}"
        await self.client.send_command(command)

    def run(self):
        """
        Запускает клиент с меню.
        """
        asyncio.run(self.display_menu())

if __name__ == "__main__":
    client_menu = ClientMenu()
    client_menu.run()
