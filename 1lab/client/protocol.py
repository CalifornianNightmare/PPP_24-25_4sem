import struct

class Protocol:
    """
    Класс для упаковки и распаковки сообщений с префиксом длины.
    """

    @staticmethod
    async def send_message(writer, message):
        """
        Отправляет сообщение клиенту с префиксом длины.
        """
        data = message.encode()
        length_prefix = struct.pack("!I", len(data))  # 4-байтовый префикс длины
        writer.write(length_prefix + data)
        await writer.drain()

    @staticmethod
    async def recv_message(reader):
        """
        Получает сообщение с префиксом длины.
        """
        length_prefix = await reader.readexactly(4)
        length = struct.unpack("!I", length_prefix)[0]
        data = await reader.readexactly(length)
        return data.decode()
