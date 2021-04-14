import unittest
from webserver import Server
from response_func import static_file_get
import requests
from serve_client import ServeClient
from threading import Thread
import json


class Tests(unittest.TestCase):
    def test_1(self):
        def test_html_response():
            resp = requests.get("http://localhost/")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.reason, 'OK')
            self.assertIn('Content-Type', resp.headers)
            self.assertIn('Content-Length', resp.headers)
            self.assertIn("<img src='http://localhost/pic'", resp.text)

        def test_pic_response():
            resp = requests.get("http://localhost/pic")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.reason, 'OK')
            self.assertIn('Content-Type', resp.headers)
            self.assertIn('Content-Length', resp.headers)
            self.assertIn('Content-Length', resp.headers)
            self.assertIn('141025', resp.headers['Content-Length'])

        with Server() as app:
            app.route_get('/',
                          lambda req: static_file_get(
                              'demo/html_pages/index.html',
                              req))
            app.route_get('/pic',
                          lambda req: static_file_get(
                              'demo/pictures/picture.jpg',
                              req))
            server_thread = Thread(target=app.start)
            server_thread.daemon = True
            server_thread.start()
            test_html_response()
            test_pic_response()

    def test_post_request(self):
        req = "POST /users?name=Vasya&age=22 HTTP/1.1"
        res = ServeClient(req, {}).serve_client()
        self.assertIs(res.status, 204)
        self.assertIs(res.reason, "Created")

        req1 = "POST /users?name=Petya&age=56 HTTP/1.1"
        res1 = ServeClient(req1, {}).serve_client()
        self.assertIs(res1.status, 204)
        self.assertIs(res1.reason, "Created")
        with open('demo/user.json', 'r') as f:
            f_str = json.load(f)
            self.assertEqual(f_str, {'/users':
                [
                    {'name': 'Vasya', 'age': '22'},
                    {'name': 'Petya', 'age': '56'}
                ]})


if __name__ == '__main__':
    unittest.main()
