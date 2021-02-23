# Дипломный проект по курсу Django

## Задание

Разработать API для интернет-магазина. Должно быть реализовано API сервиса и интерфейс администрирования. В качестве фреймворка необходимо использовать Django и Django REST Framework.


## Документация по проекту


Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```bash
manage.py makemigrations
manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```


 Примерами запросов к API в [файле requests-examples.http](./requests-examples.http)


