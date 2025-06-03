# Currency Rate App
Django проект для получения актуального курса USD/RUB через API.

## Запуск проекта
### Локально
1. Установите зависимости: `pip install -r requirements.txt`
2. Настройте API-ключ в `В .env добавьте api key https://app.exchangerate-api.com/keys/added`
3. Выполните миграции: `python manage.py migrate`
4. Запустите сервер: `python manage.py runserver`

## Эндпоинт
- GET `/get-current-usd/` — возвращает текущий курс и 10 последних запросов.