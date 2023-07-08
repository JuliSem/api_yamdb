# api_yamdb

Проект **YaMDb** собирает отзывы пользователей на различные произведения.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone "адрес клонируемого репозитория"
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

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

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Выполнить загрузку первичных данных:

```
python3 manage.py import_csv
```

Запустить проект:

```
python3 manage.py runserver
```