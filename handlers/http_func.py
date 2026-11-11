from logger import logger
from config import BYTES_SIZE, CONNECTION_TIMEOUT, READ_TIMEOUT
import socket

def http_func(client_socket, request, url):
    url = url[7:]
    host = url.split('/')[0]
    port = 80
    if ':' in host:
        host, port = host.split(':')
        port = int(port)

    # Открытие сокета для подключения к внешнему хосту

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
            remote_socket.settimeout(CONNECTION_TIMEOUT)
            try:
                remote_socket.connect((host, port))
                remote_socket.settimeout(READ_TIMEOUT)
                remote_socket.sendall(request)
                logger.info(f"Успешное подключение и отправка сообщения на {host}:{port}")
            except Exception as e:
                logger.error(f'Ошибка при подключении к {host}: {e}')
                return

            while True:
                try:
                    response = remote_socket.recv(BYTES_SIZE)
                    if not response:
                        break
                    client_socket.sendall(response)
                    logger.info("Корректная отправка ответа пользователю")
                except Exception as e:
                    logger.error(f'Ошибка при отправке ответа пользователю: {e}')
                    break
            