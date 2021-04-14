class Request:
    """Класс запроса"""
    def __init__(self, method, path, version, cookies):
        self.method = method
        self.path = path
        self.version = version
        self.cookies = cookies


def parse_request(request):
    """Парсим запрос и возвращает Request"""
    if request is not b'':
        request = str(request)
        if "GET" in request:
            request = request[2:]
        request_line = request.rstrip('\r\n')
        words = request_line.split()
        method = words[0]
        path = words[1]
        version = words[2]
        cookie = None
        if '?' in words[1]:
            i = words[1].index('?')
            cookie = parse_cookies(words[1][i + 1:])
            path = words[1][:i]
        return Request(method, path, version, cookie)


def parse_cookies(cookies_str):
    """Парсим cookie"""
    cookies = cookies_str.split('&')
    return {item.split('=')[0]: item.split('=')[1] for item in cookies}
