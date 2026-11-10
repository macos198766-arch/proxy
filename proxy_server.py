import socket
import threading
from handle import handle_client
from logger import logger
from config import HOST, PORT

# Создание самого сервера(он будет открывать сокеты в потоках для разных клиентов и запросов)
def start_proxy():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    server_address = (HOST, PORT)
    try:
        server_socket.bind(server_address)
        server_socket.listen(10)
        logger.info(f"Сервер создан успешно на {server_address}")
    except Exception as e:
        logger.critical(f"Не удалось создать сервер: {e}")

    while True:
        try:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        except Exception as e:
            logger.error(f"Ошибка при подключения клиента: {e}")

# Запуск
if __name__ == '__main__':
    start_proxy()