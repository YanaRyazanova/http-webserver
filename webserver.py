from socket import socket, SOL_SOCKET, SO_REUSEADDR
from serve_client import ServeClient
from response_func import print_http_response_info
import select
import logging
import os


class Server:
    """Основной класс веб-вервера"""
    def __init__(self, host='0.0.0.0', port=80):
        self.port = port
        self.host = host
        self.get_routes = {}
        self.server_socket = socket()
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.get_routes.clear()

    def start(self):
        """Метод, запускающий обработку запросов и отправляющий ответ"""
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        inputs = [self.server_socket]
        outputs = []
        message_queues = {}
        log_path = os.path.abspath('../requests.log')
        logging.basicConfig(filename=log_path, level=logging.INFO)
        try:
            while True:
                (read_ready, write_ready, errors) = select.select(inputs,
                                                                  outputs,
                                                                  inputs,
                                                                  1.0)
                for sock in read_ready:
                    if sock is self.server_socket:
                        (user_socket, address) = sock.accept()
                        user_socket.setblocking(False)
                        inputs.append(user_socket)
                        message_queues[user_socket] = []
                    else:
                        request = sock.recv(65535)
                        logging.info(request)
                        if request:
                            message_queues[sock].append(request)
                            if sock not in outputs:
                                outputs.append(sock)
                        else:
                            if sock in outputs:
                                outputs.remove(sock)
                            inputs.remove(sock)
                            # sock.close()
                            del message_queues[sock]
                for sock in write_ready:
                    i = len(message_queues[sock])
                    if i == 0:
                        outputs.remove(sock)
                    else:
                        next_message = message_queues[sock][i - 1]
                        resp_content = ServeClient(
                            next_message, self.get_routes).serve_client()
                        if resp_content is not None:
                            print_http_response_info(sock, resp_content)
                            message_queues[sock].remove(next_message)
                for sock in errors:
                    inputs.remove(sock)
                    if sock in outputs:
                        outputs.remove(sock)
                    sock.close()
                    del message_queues[sock]
        except Exception as e:
            if (e == "<socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>"):
                self.start()
            else:
                print(f"Something goes wrong: {e}")
        finally:
            self.server_socket.close()

    def route_get(self, route, path):
        """Метод, добавляющий обработчик запроса 'GET'"""
        if route not in self.get_routes:
            self.get_routes[route] = path
