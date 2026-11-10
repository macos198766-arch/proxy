from handlers.http_func import http_func
from handlers.https_func import https_func
from logger import logger
from config import BYTES_SIZE, READ_TIMEOUT

def handle_client(client_socket):
    client_socket.settimeout(READ_TIMEOUT)
    try:
        request = client_socket.recv(BYTES_SIZE)
        logger.info(f"Запрос от клиента({client_socket})")
        if not request:
            return
    except Exception as e:
        logger.error(f"Ошибка при запросе от клиента: {e}")
        return
    
        # Парсинг запроса
    try:
        first_line = request.split(b'\n')[0].decode('utf-8', errors='ignore')
        url = first_line.split(' ')[1]
    except IndexError:
        logger.error("Кривой запрос")
        return
    

#----Обработка HTTP
    if url.startswith('http://'):
        http_func(client_socket, request, url)

#----Обработка HTTPS   
    elif first_line.startswith('CONNECT'):
        https_func(client_socket, url)

    logger.info("Закрытие соединения")