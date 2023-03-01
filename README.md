# Приложение для создания постов

> Примечание
> - Знаю, что файл .env и саму БД не надо загружать в git и в docker, но решил так сделать, чтобы проще посмотреть проект, если кто-то захочет

### Используемые библиотеки:

- Flask, flask [-login, -migrate, -paginate, -humanize, -admin, -debugtoolbar, -sqlalchemy, -wtf ]
- alembic, python-slugify, python-dotenv, Isort, flake8
## Варианты установки:

1. С помощью Docker
2. В ручную

### 1 вариант

1. У вас должен быть установлен Docker на компьютере( https://www.docker.com/ )
2. `git clone https://github.com/romaha57/flask_blog.git`
3. `docker build -t app_blog .`
4. `docker run -d -p 8000:8000 app_blog`


### 2 вариант

1. `git clone https://github.com/romaha57/flask_blog.git`
2. `pip install -r requirements.txt`


## Возможности приложения

- Регистрация, авторизация
- Админка(flask-admin)
- Создание категории и тегов для администраторов сайта
- Создание постов и комментариев для авторизированных пользователей
- Просмотр постов, поиск по названию, фильтрация по категориям и тегам


Буду рад, если у кого-то будут предложения по исправлению: 

Телеграм: @roma_junior