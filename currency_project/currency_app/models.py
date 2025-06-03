from django.db import models

class ExchangeRate(models.Model):
    usd_to_rub = models.FloatField()  # Курс USD/RUB
    timestamp = models.DateTimeField(auto_now_add=True)  # Время запроса

    class Meta:
        ordering = ['-timestamp']  # Сортировка по убыванию времени

    def __str__(self):
        return f"USD/RUB: {self.usd_to_rub} at {self.timestamp}"