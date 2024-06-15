# Тестовое задание на позицию Python Developer от MADSOFT
## Задание:

Разработайте веб-приложение на Python, используя FastAPI, которое предоставляет API для работы с коллекцией мемов.
Приложение должно состоять из двух сервисов: сервис с публичным API с бизнес-логикой и сервис для работы с
медиа-файлами, используя S3-совместимое хранилище (н-р, MinIO).

## Функциональность:

●  GET /memes: Получить список всех мемов (с пагинацией).

●  GET /memes/{id}: Получить конкретный мем по его ID.

●  POST /memes: Добавить новый мем (с картинкой и текстом).

●  PUT /memes/{id}: Обновить существующий мем.

●  DELETE /memes/{id}: Удалить мем.

## Требования:

●  Используйте реляционную СУБД для хранения данных.

●  Обеспечьте обработку ошибок и валидацию входных данных.

●  Используйте Swagger/OpenAPI для документирования API.

●  Напишите хотя бы несколько unit-тестов для проверки основной функциональности.

●  Напишите Readme, из которого понятна функциональность проекта и инструкция по локальному запуску для разработки.

●  Проект должен состоять минимум из: 1 сервис с публичным API, 1 сервис с приватным API для изображений,
1 сервис СУБД, 1 сервис S3-storage.

●  Напишите docker-compose.yml для запуска проекта.


## Ожидаемый результат:

● Публичный git-репозиторий с проектом согласно перечисленным требованиям.

## Использование:

1. Установите все зависимости, указанные в файле requirements.txt.
2. Запустите проект с помощью docker-compose:
```docker-compose up```
3. Откройте Swagger UI в браузере:
```http://localhost:8000/docs```
4. Используйте API для работы с коллекцией мемов.

## Тестирование:

1. Запустите тесты с помощью команды:
```pytest```
2. Проверьте, что все тесты пройдены.

## Документация:

1. Swagger/OpenAPI документация доступна по адресу:
```http://localhost:8000/docs```
2. Файл README.md содержит информацию о функциональности проекта и инструкции по локальному запуску для разработки.

## Errors:

Проект сырой нужно дорабатывать на данный момент существуют две основные ошибки:
1. При загрузке мемов в minIO(запуск файла: media/main.py)
TimeoutError: [WinError 10060] Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое 
время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже 
подключенного компьютера
2. В логе контейнера с запущенным проектом при вызове api:
GET /memes HTTP/1.1" 500 Internal Server Error
qlalchemy.exc.ArgumentError: Column expression, FROM clause, or other columns clause element expected, 
got <class 'app.api.models.Meme'>.

## Полезная информация

https://github.com/sixfwa/fastapi-memes/tree/main - проект для анализа на будущее.