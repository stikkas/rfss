# Сайт "Совет судей Российской федерации"

*Описана установка, настройка и обслуживание на debian-like дистрибутив.
Работа с другими дистрибутивами может немного отличаться, курите howtos, mans и подобные штуки.
Крайне рекомендуем использовать **virtualenv**.
Все операции проводятся под учетной записью root или пользователя имеющего права на выполнение нижеописанных операций.
Команды специфичны для bash/sh/zsh окружения.*

### `Установка`

##### *Установка virtualevn*

```sh
$ sudo apt-get install python-virtualenv
$ export BASE_DIR=/home/portal/apps/ssrf
$ export PY_LIB=$BASE_DIR/env
$ mkdir -p $BASE_DIR $PY_LIB
$ cd $BASE_DIR
$ virtualenv env
$ source env/bin/activate
```

##### *Установка дистрибутива*

*Перед установкой необходимо добавить ssh ключ для django_tinymce, 
т.к. он настроен на ssh протокол*

```sh
$ hg clone https://gas_pravosudie@bitbucket.org/gas_pravosudie/django_ssrf src
$ pip install -U -r src/requirements.txt
$ sudo apt-get install libmysqlclient-dev
$ pip install MySQL-python
```

##### *Создание базы данных*

```sh
$ mysql -u root -e "create database ssrf default charset utf8"
$ mysql -u root -e "grant all privileges on ssrf.* to 'ssrf'@'localhost' identified by 'ssrf'"
$ mysql -u ssrf -pssrf ssrf < data_file.sql
```

##### *Настройка подключения к базе данных*

```sh
$ cat > src/web/local_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ssrf',                      
        'USER': 'ssrf',                      
        'PASSWORD': 'ssrf',                  
        'HOST': 'localhost',             
        'PORT': '',                      
    }
}
```

##### *Создаем рабочие папки*

```sh
$ mkdir -p logs
$ mkdir -p src/web/search_index/pages
$ mkdir -p src/web/public/{media,static}
$ cp -R /where_is_our_media_files/* src/web/public/media
```

Бэки базы и загружаемых файлов: /home/portal/backs/

Структура папки с проектом:
logs/ - логи gunicorn и периодических задач, причем логи не ротируемые, т.е. нужно чистить )
env/ - virtualenv
run.sh - скрипт для запуска supervisord'ом, тут указываются вывод логов и запуск gunicorn
public/ - статика, обслуживается nginx'ом
public/media/ - загружаемые пользователями файлы
public/static/ - файлы генерируемые командой collectstatic

Деплой обычно следующий:
$ cd {home_project}/src
$ hg pull -u

если нужно:
$ python manage.py migrate
$ python manage.py collectstatic
добавляем в крон периодические задачи

после перезапускаем инстансы:
$ sudo supervisord restart [ssrf.ru|vkks.ru|vekrf.ru]

Не забыть добавить в периодические задачи отправку обращений граждан (модуль letters).
Так-же в админке ({site_url}/admin/), нужно будет указать почтовые ящики для каждого региона куда будут направляться эти обращения.

### `Обновление`


