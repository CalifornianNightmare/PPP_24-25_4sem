import os
import json
import asyncio
from config import APPS_DIR, APPS_REGISTRY

REAL_DIR = os.path.dirname(os.path.realpath(__file__))

class AppManager:
    """
    Управляет программами: добавляет, удаляет, запускает, останавливает и отслеживает их статус.
    """

    def __init__(self):
        self.apps = {}
        self.load_registry()

    def load_registry(self):
        """
        Загружает реестр программ из JSON-файла.
        """
        if os.path.exists(os.path.join(REAL_DIR, APPS_REGISTRY)):
            with open(os.path.join(REAL_DIR, APPS_REGISTRY), "r", encoding="utf-8") as f:
                self.apps = json.load(f)
        else:
            self.apps = {}

    def save_registry(self):
        """
        Сохраняет реестр программ в JSON-файл.
        """
        with open(os.path.join(REAL_DIR, APPS_REGISTRY), "w", encoding="utf-8") as f:
            json.dump(self.apps, f, indent=4)

    async def add_app(self, appname, filename, applaunch, interval, filecontents):
        """
        Добавляет программу, создаёт файл и запускает выполнение с указанным интервалом.
        """
        app_path = os.path.join(os.path.join(REAL_DIR, APPS_DIR), appname)
        os.makedirs(app_path, exist_ok=True)

        file_path = os.path.join(app_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(filecontents)

        self.apps[appname] = {
            "filename": filename,
            "applaunch": applaunch,
            "interval": int(interval),
            "status": "running",
            "output": "",
        }
        self.save_registry()

        asyncio.create_task(self.run_app(appname))

        return f"message Программа {appname} добавлена и запущена."

    async def remove_app(self, appname):
        """
        Удаляет программу и её файлы.
        """
        if appname in self.apps:
            app_path = os.path.join(os.path.join(REAL_DIR, APPS_DIR), appname)
            if os.path.exists(app_path):
                for file in os.listdir(app_path):
                    os.remove(os.path.join(app_path, file))
                os.rmdir(app_path)

            del self.apps[appname]
            self.save_registry()
            return f"message Программа {appname} удалена."
        return "message Программа не найдена."

    async def start_app(self, appname):
        """
        Запускает приостановленную программу.
        """
        if appname in self.apps and self.apps[appname]["status"] == "stopped":
            self.apps[appname]["status"] = "running"
            self.save_registry()
            asyncio.create_task(self.run_app(appname))
            return f"message Программа {appname} запущена."
        return "message Программа не найдена или уже запущена."

    async def stop_app(self, appname):
        """
        Останавливает выполнение программы.
        """
        if appname in self.apps and self.apps[appname]["status"] == "running":
            self.apps[appname]["status"] = "stopped"
            self.save_registry()
            return f"message Программа {appname} остановлена."
        return "message Программа не найдена или уже остановлена."

    async def run_app(self, appname):
        """
        Запускает программу в цикле с указанным интервалом.
        """
        while appname in self.apps and self.apps[appname]["status"] == "running":
            try:
                result = await self.execute_program(appname)
                self.apps[appname]["output"] = result
                self.save_registry()
            except Exception as e:
                self.apps[appname]["output"] = f"Ошибка: {str(e)}"
                self.save_registry()
            await asyncio.sleep(self.apps[appname]["interval"] / 1000)

    async def execute_program(self, appname):
        """
        Выполняет команду программы и возвращает результат.
        """
        cmd = self.apps[appname]["applaunch"]
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=os.path.join(REAL_DIR, 'apps', appname)
        )
        stdout, stderr = await process.communicate()
        return stdout.decode() if stdout else stderr.decode()

    async def list_apps(self):
        """
        Возвращает список программ.
        """
        return list(self.apps.keys())

    async def get_app_result(self, appname):
        """
        Возвращает результат работы программы.
        """
        if appname in self.apps:
            return f"message {self.apps[appname]['output']}"
        return "message Программа не найдена."
