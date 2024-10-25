from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.exceptions import ValidationError

from .models import Product, Type, Price


class TypeSerializer(ModelSerializer):
    """Сериализатор для модели Type"""

    class Meta:
        model = Type
        fields = ('id', 'name', 'description')


class PriceSerializer(ModelSerializer):
    """Сериализатор для модели Price"""

    class Meta:
        model = Price
        fields = ('id', 'currency', 'amount')


class ProductSerializer(ModelSerializer):
    """Сериализатор для модели Product"""
    type = PrimaryKeyRelatedField(queryset=Type.objects.all())
    price = PrimaryKeyRelatedField(queryset=Price.objects.all())

    def validate_barcode(self, value):
        """Валидация для проверки уникальности штрихкода"""
        if self.instance:
            if Product.objects.filter(barcode=value).exclude(
                    id=self.instance.id).exists():
                raise ValidationError(
                    "Product with this barcode already exists.")
        else:
            if Product.objects.filter(barcode=value).exists():
                raise ValidationError(
                    "Product with this barcode already exists.")
        return value

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity', 'barcode', 'updated_at',
                  'type')
