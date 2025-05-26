# Cashflow — учёт доходов и расходов

Простой Django-проект для учёта финансов с удобным интерфейсом, поддержкой категорий и подкатегорий, а также возможностью фильтрации и удаления записей.

## Возможности

- Учёт доходов и расходов
- CRUD-записи с привязкой к категориям и подкатегориям
- Ajax-загрузка категорий по типу (доход/расход)
- Удобный Bootstrap-интерфейс
- Подтверждение удаления записей
- Управление категориями и подкатегориями

---

## Запуск проекта

### 1. Клонируйте репозиторий
### 2. Создайте и активируйте виртуальное окружение
 - python -m venv venv
 - source venv/bin/activate        # Linux/macOS
 - venv\Scripts\activate           # Windows
### 3. Установите зависимости
 - pip install -r requirements.txt
### 4. Настройка базы данных (PostgreSQL)
Создайте базу данных и пользователя:
    CREATE DATABASE myprojectdb;
    CREATE USER myprojectuser WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myprojectuser;
Обновите настройки в settings.py:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'myprojectdb',
            'USER': 'myprojectuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
### 5. Примените миграции и создайте суперпользователя (если нужно)
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py createsuperuser
### 6. Запустите сервер
  - python manage.py runserver
### Перейдите в браузере: http://127.0.0.1:8000/

### Зависимости
  Python 3.10+
  Django
  psycopg2-binary (для PostgreSQL)
  Bootstrap 5 (через CDN)

---

Скриншоты лежат в папке screenshots/ в корне проекта
