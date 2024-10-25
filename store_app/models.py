from django.db import models


class Type(models.Model):
    """Модель, представляющая тип товара с его описанием"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    """Модель, представляющая цену товара с указанием валюты"""

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('RUB', 'Russian Ruble'),
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} {self.currency}"


class Product(models.Model):
    """Модель, представляющая товар с ценой, количеством и типом"""

    name = models.CharField(max_length=255)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    barcode = models.CharField(max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
