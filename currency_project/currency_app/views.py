import requests
import time
from django.http import JsonResponse
from django.core.cache import cache
from .models import ExchangeRate


def get_usd_to_rub():
    api_key = "8beacbecb6c9379430ead39d"  # Замените на ваш ключ
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['conversion_rates']['RUB']
    except requests.RequestException as e:
        return None


def get_current_usd(request):
    # Проверяем время последнего запроса
    last_request_time = cache.get('last_request_time', 0)
    current_time = time.time()

    if current_time - last_request_time < 10:
        # Если прошло меньше 10 секунд, возвращаем последний сохраненный курс
        latest_rate = ExchangeRate.objects.first()
        if not latest_rate:
            return JsonResponse({'error': 'No data available'}, status=503)
        usd_to_rub = latest_rate.usd_to_rub
    else:
        # Запрашиваем новый курс
        usd_to_rub = get_usd_to_rub()
        if usd_to_rub is None:
            return JsonResponse({'error': 'Failed to fetch exchange rate'}, status=503)

        # Сохраняем курс в базе
        ExchangeRate.objects.create(usd_to_rub=usd_to_rub)
        cache.set('last_request_time', current_time, timeout=3600)

    # Получаем 10 последних запросов
    last_10_rates = ExchangeRate.objects.all()[:10]
    history = [{'usd_to_rub': rate.usd_to_rub, 'timestamp': rate.timestamp} for rate in last_10_rates]

    return JsonResponse({
        'current_usd_to_rub': usd_to_rub,
        'history': history
    })