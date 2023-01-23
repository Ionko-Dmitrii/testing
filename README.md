# Testing

# Описание проекта
Проект для тестирования пользователей

# Как поднять локально проект?
Зависимости:
- PostgreSQL
- Python 3.9
- Django 2.2

Добавить `settings_local.py` для кастомных настроек 

## Переменные окружения для продакшена и локальной разработки:
| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `DJANGO_SECRET_KEY`  | secret key  | secret-key              |
| `DJANGO_DEBUG`  | Debug mode True or False  | True              |
| `DJANGO_ALLOWED_HOST`| Allowed host | [] |
| `DEFAULT_DATABASE_URL`  | postgres://user:password@host:port/database_name | postgres://db_user:db_password@localhost:5432/db_name |

## Последовательность действий
```.bash
    $ virtualenv venv
    $ pip install -r requirements.txt
    $ Добавить `.env` файл для настроек
```
Необходимо создать в PostgreSQL создать БД:
```.bash
    $ sudo -u postgres psql
    $ create database testing_db encoding 'UTF-8';
    $ \q
```
После создания БД, необходимо применить миграцию, после запуск тестового сервера:
```.bash
    $ python manage.py migrate
    $ python manage.py runserver
```
Если все успешно то переходите по ссылке ==> `http://locahost:8000`

# Как поднять проект в docker?
Зависимости:
- docker
- docker-compose
- .env_db

## Переменные окружения для базы данных docker .env_db:
| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `POSTGRES_DB`  | db name  | testing              |
| `POSTGRES_USER`  | db user  | postgres              |
| `POSTGRES_PASWORD`| db password | postgres |

После создания .env_db и установки зависимостей:
```.bash
    $ docker-compose build web
    $ docker-compose up -d
```

Если все успешно то переходите по ссылке ==> `http://locahost:8000`