from logger import logger
import threading
from config import BYTES_SIZE, CONNECTION_TIMEOUT, READ_TIMEOUT
import socket

def https_func(client_socket, url):
    host, port = url.split(':')
    port = int(port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
            remote_socket.settimeout(CONNECTION_TIMEOUT)
            remote_socket.connect((host, port))
            logger.info(f"Успешное подключение к {host}:{port}")
            client_socket.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')

            def tunnel_stream(source, dest):
                try:
                    source.settimeout(READ_TIMEOUT)
                    while True:
                        data = source.recv(BYTES_SIZE)
                        if not data:
                            break
                        dest.sendall(data)
                except (ConnectionAbortedError, ConnectionResetError, socket.timeout) as e:
                    logger.debug(f"Туннель завершён штатно: {e}")
                except Exception as e:
                    logger.error(f"Ошибка туннеля: {e}")
            t1 = threading.Thread(target=tunnel_stream, args=(client_socket, remote_socket), daemon=True)
            t2 = threading.Thread(target=tunnel_stream, args=(remote_socket, client_socket), daemon=True)
            t1.start(); t2.start()
            t1.join(); t2.join()

    except Exception as e:
        logger.error(f"Ошибка туннеля для {host}: {e}")
    finally:
        logger.info("Туннель закрыт")
