from webserver import Server
from response_func import static_file_get, indexing_get
from my_response import Response
import os


def unknown_get(req):
    """Метод, возвращающий ответ для статического запроса"""
    content_type = 'text/html'
    response_text = str(str(req.method) + str(req.path) + str(req.cookies))
    body = response_text.encode('iso-8859-1')
    headers = {
        'Content-Type': content_type,
        'Content-Length': len(body),
    }
    return Response("200", "OK", headers, body)


if __name__ == '__main__':
    try:
        with Server(port=80) as app:
            app.route_get('/',
                          lambda req: static_file_get('html_pages/index.html',
                                                      req))
            app.route_get('/pic',
                          lambda req: static_file_get('pictures/picture.jpg',
                                                      req))
            app.route_get('/debug_get',
                          lambda req: unknown_get(req))
            app.route_get('/demo',
                          lambda req: indexing_get(req))
            app.start()
    except KeyboardInterrupt:
        pass
