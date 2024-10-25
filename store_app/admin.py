from django.contrib import admin
from .models import Product, Type, Price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Администраторская модель для управления продуктами"""

    list_display = ('name', 'quantity', 'barcode', 'price', 'updated_at',
                    'type')
    search_fields = ('name', 'barcode')
    list_filter = ('type',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Администраторская модель для управления типами продуктов"""

    list_display = ('name', 'description')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """ Администраторская модель для управления ценами"""

    list_display = ('amount', 'currency')
