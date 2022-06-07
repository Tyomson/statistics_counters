# Statistics counters - Инструкция по развертыванию

## Расположение и доступ

После выгрузки проекта в рабочую директорию, 
перед сборкой необходимо настроить env-файлы, 
содержащие ключи доступа к связанным с проектом сервисам.

Их можно сформировать из имеющихся в проекте файлов `.env.example`

Для `api.env`:
```
DB_URL=ключи подключения к базе данных, сформированные в url-строку
EXTERNAL_DB_URL=внешние ключи подключения к базе данных, сформированные в url-строку
SENTRY_URL=ссылка на кабинет sentry.io
```
Для `mysql.env`:
```
MYSQL_USER=логин подключения к базе данных
MYSQL_PASSWORD=пароль подключения к базе данных
MYSQL_ROOT_PASSWORD=мастер-пароль базы данных
MYSQL_DATABASE=имя базы данных
```

## Запуск

Переходим в рабочую директорию и собираем контейнеры
```
docker-compose up
```

Просмотр логов:  
`docker-compose logs`

## Документация API

Интерактивная документация доступна по адресу:
`http://адрес.сервера/docs`