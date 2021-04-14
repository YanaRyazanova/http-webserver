ЗАДАЧА: Webserver
АВТОР: Рязанова Яна Андреевна ФТ-202
ОПИСАНИЕ:
Веб-сервер, имеющий функции route_static() и start.
По запросу "http://localhost/" возвращает html-страничку;
по запросу "http://localhost/pic" возвращает картинку.
API:
        with Server() as app:
            app.route_static('/pic', static_file('pictures/picture.jpg')) - настраиваем раздачу статических файлов
            app.route_static('/sum', lambda a: sum(a)) - настраиваем произвольные обработчики запросов
            app.start() - запускаем сервер