import socket
import threading
import logging
import sys

# Базовая конфигурация логов
file_handler = logging.FileHandler("proxy.log", encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s – %(name)s – %(levelname)s – %(message)s',
    handlers=[file_handler, console_handler],
)

# Функция потока, получение http/https запроса от клиента
def handle_client(client_socket):
    request = client_socket.recv(4096)
    logging.info(f"Запрос от клиента({client_socket}): {request.decode('utf-8')}")

    # Парсинг запроса
    first_line = request.split(b'\n')[0].decode('utf-8', errors='ignore')
    url = first_line.split(' ')[1]

#----Обработка HTTP
    if url.startswith('http://'):
        url = url[7:]
        host = url.split('/')[0]
        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)

        # Открытие сокета для подключения к внешнему хосту
        try:
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((host, port))
            logging.info(f"Успешное подключение к {host}:{port}")
        except Exception as e:
            logging.error(f"Ошибка на этапе подключения к {host}:{port}: {e}")
            client_socket.close()
            return
    
        # Отправка изначального http запроса сокету 
        remote_socket.send(request)

        # Отправка ответа от сайта клиенту
        try:
            while True:
                response = remote_socket.recv(4096)
                if not response:
                    break
                client_socket.send(response)
            logging.info("Корректная отправка ответа пользователю")

        except Exception as e:
            logging.error(f"Ошибка на этапе отправки данных пользователю: {e}")

        # Закрытие всех сокетов
        remote_socket.close()
        client_socket.close()

#----Обработка HTTPS   
    elif first_line.startswith('CONNECT'):
        host, port = url.split(':')
        port = int(port)
        try:
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((host, port))
            logging.info(f"Успешное подключение к {host}:{port}")
            client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')

            def tunnel_stream(source, dest):
                try:
                    while True:
                        data = source.recv(4096)
                        if not data:
                            break
                        dest.sendall(data)
                except Exception:
                    pass
            t1 = threading.Thread(target=tunnel_stream, args=(client_socket, remote_socket))
            t2 = threading.Thread(target=tunnel_stream, args=(remote_socket, client_socket))
            t1.start(); t2.start()
            t1.join(); t2.join()


        except Exception as e:
            logging.error(f"Ошибка туннеля: {e}")
            client_socket.close()
            remote_socket.close()
            logging.info('Туннель закрыт')
            return

        


    logging.info("Закрытие соединения")

# Создание самого сервера(он будет открывать сокеты в потоках для разных клиентов и запросов)
def start_proxy():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    server_address = ('localhost', 8888)
    try:
        server_socket.bind(server_address)
        server_socket.listen(10)
        logging.info(f"Сервер создан успешно на {server_address}")
    except Exception as e:
        logging.critical(f"Не удалось создать сервер: {e}")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Запуск
if __name__ == '__main__':
    start_proxy()