from my_request import parse_request
import json
from my_response import Response
from response_func import create_post_resp
import os


class ServeClient:
    """Класс, обрабатывающий запрос"""
    def __init__(self, request, get_routes):
        self.get_routes = get_routes
        self.request = parse_request(request)

    def serve_client(self):
        """Основной метод, отправляющий текст ответа"""
        response_content = self.handler_request_route()
        if response_content is not None:
            return response_content
        return None

    def handler_request_route(self):
        """Выбираеи обработчик ответа: картинка или произвольный"""
        if self.request.method == 'GET':
            this_path = self.request.path
            if this_path in self.get_routes:
                return self.get_routes[this_path](self.request)
            else:
                return None
        if self.request.method == 'POST':
            return self.handle_post()

    def handle_post(self):
        try:
            json_path = os.path.abspath('demo/user.json')
            with open(json_path, 'r') as f:
                f_str = f.read()
                if len(f_str) == 0:
                    guests = {}
                else:
                    guests = json.loads(f_str)
                if self.request.path not in guests:
                    guests[self.request.path] = []
                guests[self.request.path].append(self.request.cookies)
            with open(json_path, 'w') as f:
                json.dump(guests, f)
            return create_post_resp(204, "Created")
        except Exception as e:
            print(f"Something goes wrong: {e}")
            return create_post_resp(505, "Error")

    def arbitrary_get_handler(self, func):
        """Обработка произвольного запроса"""
        return func(self.get_routes[self.request.path], self.request.cookies)
