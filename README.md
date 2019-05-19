#Описание тестового задания.

### ДЛЯ BACKEND-РАЗРАБОТЧИКА

Уровень - junior.

Создать Django-приложение для аплоада и ресайза изображений.

### Приложение должно состоять из:

- индексная страница - /

    Страница должна содержать список изображений и ссылку на страницу аплоада

- страница аплоада - /upload/

    Должна содержать форму с двумя полями:

    1. file - для аплоада файлом
    2. url - для загрузки по url

    Должна валидироваться заполненность только одного поля формы

- страница изображения - /<image_hash>/?query_params

    Страница содержит изображение. Если нет GET-параметров, то оно приходит с бэка неизменённым. Могут присутствовать три GET-параметра:

    1. width - поле для изменения ширины изображения
    - width - ширина
    - height - высота
    - size - максимальный размер в байтах

    Они могут присутствовать как по отдельности, так и вместе.

    При наличии параметром необходимо произвести ресайз***** или ухудшение качества изображения. **Не изменять исходное изображение.** Использовать кэширование, чтобы не генерировать новое изображение при повторных запросах.

    *****резайз(англ. resize) - изменение размеров (высота/ширина)

## Требования

- Описать процесс локального запуска. Проект должен запускаться одной командой. Скрипт это будет или management-команда остаётся на усмотрение кандидата.
- Зависимости расположить в файле requirements.txt
- В качестве БД использовать SQLite.

## Плюсом будет:

- Покрытие кода тестами
- В свободной форме описать способ деплоя приложения

# ОПИСАНИЕ ДЕПЛОЯ (ОТВЕТ)

Установка необходимых пакетов:
* apt-get update
* apt-get upgrade
* apt-get install nginx
* apt-get install python3-dev python3-setuptools
* apt-get install python3-venv
* apt-get install git nano
* apt-get install python-dev default-libmysqlclient-dev
* apt-get install python-dev gcc
--- 

В папку проекта код и виртуальное окружение:
* git clone https://github.com/Golhoper/test-for-IdaProject.git
* python3 -m venv venv
--- 

Входим в виртуальное окружение:
* source venv/bin/activate
* pip3 install --upgrade pip
* pip3 install -r requirements.txt
* pip3 install uwsgi (опущу процесс теста работы uwsgi в виртуальном окружении)
* python3 manage.py collectstatic

* mkdir media
* mkdir deployment ##папка, где собираются конфиги проекта

* rm -rf /etc/nginx/sites-enabled/default
---

В папке deployment:

nano uwsgi_params (вставляем в файл ниже)
```
	uwsgi_param  QUERY_STRING       $query_string;
	uwsgi_param  REQUEST_METHOD     $request_method;
	uwsgi_param  CONTENT_TYPE       $content_type;
	uwsgi_param  CONTENT_LENGTH     $content_length;

	uwsgi_param  REQUEST_URI        $request_uri;
	uwsgi_param  PATH_INFO          $document_uri;
	uwsgi_param  DOCUMENT_ROOT      $document_root;
	uwsgi_param  SERVER_PROTOCOL    $server_protocol;
	uwsgi_param  REQUEST_SCHEME     $scheme;
	uwsgi_param  HTTPS              $https if_not_empty;

	uwsgi_param  REMOTE_ADDR        $remote_addr;
	uwsgi_param  REMOTE_PORT        $remote_port;
	uwsgi_param  SERVER_PORT        $server_port;
	uwsgi_param  SERVER_NAME        $server_name;
```

nano ida_nginx.conf (вставляем в файл ниже)
```
upstream django {
    server unix:///home/django/test-for-IdaProject/uwsgi_nginx.sock; 
}

server {
    listen      80;
    server_name 78.140.221.65;
    charset     utf-8;
    client_max_body_size 75M;

    location /media  {
	alias /home/django/test-for-IdaProject/media;
    }

    location /static {
	alias /home/django/test-for-IdaProject/static;
    }

    location / {
	uwsgi_pass  django;
	include     /home/django/test-for-IdaProject/deployment/uwsgi_params;
    }
}

```

nano ida_uwsgi.ini (вставляем в файл ниже)
```
[uwsgi]

chdir           = /home/django/test-for-IdaProject
module          = IdaProject.wsgi
home            = /home/django/test-for-IdaProject/venv
master          = true
processes       = 10
socket          = /home/django/test-for-IdaProject/uwsgi_nginx.sock
chmod-socket    = 666
vacuum          = true
env             = DEBUG_MODE=False
```

--- ---

Чтобы nginx увидел конфиг:

* sudo ln -s /home/django/test-for-IdaProject/deployment/ida_nginx.conf /etc/nginx/sites-enabled
* service supervisor restart
--- ---

Если запускать uwsgi в режиме императора: 

* sudo mkdir /etc/uwsgi
* sudo mkdir /etc/uwsgi/vassals

* sudo ln -s /home/django/test-for-IdaProject/deployment/ida_uwsgi.ini /etc/uwsgi/vassals/
--- ---

Включаем супервизора:

* apt-get install supervisor
* echo_supervisord_conf > /etc/supervisord.conf

* nano /etc/supervisor/conf.d/ida.conf (в него ниже)
```
	[program:ida]
	command=uwsgi --emperor "/home/django/test-for-IdaProject/deployment/ida_uwsgi.ini"
	stdout_logfile=/home/django/test-for-IdaProject/deployment/uwsgi.log
	stderr_logfile=/home/django/test-for-IdaProject/deployment/uwsgi_err.log
	autostart=true
	autorestart=true
```
* supervisorctl reread
* supervisorctl update
* service supervisor stop
* service supervisor start
---

Теперь должно все работать.