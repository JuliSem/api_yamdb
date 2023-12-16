# api_yamdb

Проект **YaMDb** - API для сайта, который собирает отзывы пользователей 
на различные произведения, фильмы, музыку.

### Стек проекта:

- Python 3.9.10
- Django 3.2
- Django REST Framework 3.12.4
- Simple-JWT
- SQlite
- pytest

### Как запустить проект:

<br>1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone "адрес клонируемого репозитория"
```

```
cd api_yamdb
```

<br>2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

<br>3. Установить и обновить пакетный менеджер:

```
python3 -m pip install --upgrade pip
```

<br>4. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

<br>5. Перейти в папку **api_yamdb**(где находится файл manage.py) и 
выполнить миграции:

```
cd api_yamdb
```

```
python3 manage.py migrate
```

<br>6. Выполнить загрузку первичных данных:

```
python3 manage.py import_csv
```

<br>7. Запустить проект:

```
python3 manage.py runserver
```
### Примеры запросов:

* Регистрация пользователя с получением кода доступа на e-mail (POST-запрос):

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

* Получение JWT-токена в обмен на username и confirmation code (POST-запрос):

```
http://127.0.0.1:8000/api/v1/auth/token/
```

* Получение списка всех произведений (GET-запрос):

```
http://127.0.0.1:8000/api/v1/titles/
```

* Получение списка всех категорий (GET-запрос):

```
http://127.0.0.1:8000/api/v1/categories/
```

С другими запросами к API можно ознакомиться в документе ReDoc: 
```http://127.0.0.1:8000/redoc/```

### Авторы проекта:

* Семёнова Юлия (GitHub: JuliSem) - team lead
* Адылов Тимур (GitHub: atcoom)
* Янов Максим (GitHub: Maxway07)