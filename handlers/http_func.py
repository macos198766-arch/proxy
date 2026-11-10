from logger import logger
from config import BYTES_SIZE, CONNECTION_TIMEOUT, READ_TIMEOUT
import socket

def http_func(client_socket, request, url):
    remote_socket = None
    url = url[7:]
    host = url.split('/')[0]
    port = 80
    if ':' in host:
        host, port = host.split(':')
        port = int(port)

    # Открытие сокета для подключения к внешнему хосту
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.settimeout(CONNECTION_TIMEOUT)
        remote_socket.connect((host, port))
        remote_socket.settimeout(READ_TIMEOUT)
        logger.info(f"Успешное подключение к {host}:{port}")
    except Exception as e:
        logger.error(f"Ошибка на этапе подключения к {host}:{port}: {e}")
        client_socket.close()
        return
    
    # Отправка ответа от сайта клиенту
    try:
        # Отправка изначального http запроса сокету 
        remote_socket.sendall(request)
        while True:
            response = remote_socket.recv(BYTES_SIZE)
            if not response:
                break
            client_socket.send(response)
        logger.info("Корректная отправка ответа пользователю")

    except Exception as e:
        logger.error(f"Ошибка на этапе отправки данных пользователю: {e}")
    finally:
        if remote_socket is not None:
            remote_socket.close()
        client_socket.close()