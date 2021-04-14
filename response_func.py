from my_response import Response
import re
import os


def create_post_resp(statuc, reason):
    headers = {
        'Connection': 'Keep-Alive'
    }
    return Response(statuc, reason, headers)


def indexing_get(req):
    cur_files = os.listdir()
    res = [file for file in cur_files]
    body_str = ''
    for item in res:
        if "pycache" in item:
            continue
        body_str += str(item) + '\n'
    body_str = str(body_str).encode('iso-8859-1')
    headers = {
        'Content-type': 'text',
        'Content-Length': len(body_str),
        'Connection': 'Keep-Alive'
    }
    return Response("200", "OK", headers, body_str)


def static_file_get(path, req):
    """Метод, возвращающий ответ для статического запроса"""
    body = encode_response_body(path)
    content_type = 'image'
    if '.html' in path:
        content_type = 'text/html; charset=iso-8859-1'
    headers = {
        'Content-Type': content_type,
        'Content-Length': len(body),
        'Connection': 'Keep-Alive'
        }
    return Response("200", "OK", headers, body)


def print_http_response_info(conn, resp):
    """Метод, который отправляет файл в браузер по сокету,
    чтобы страница корректно отображалась в браузере"""
    with conn.makefile('wb') as wfile:
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))
        if resp.headers:
            for key, value in resp.headers.items():
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
        wfile.write(b'\r\n')
        if resp.body:
            wfile.write(resp.body)
        wfile.flush()


def encode_response_body(response_body):
    """Кодируем ответ"""
    if isinstance(response_body, str) and re.search(r'/*.', response_body):
        with open(response_body, 'rb') as file:
            str_response = file.read()
            encoded_response = str_response
    else:
        encoded_response = str(response_body).encode('iso-8859-1')
    return encoded_response