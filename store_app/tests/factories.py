import factory

from store_app.models import Type, Price, Product


class TypeFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания экземпляров модели Type"""

    class Meta:
        model = Type

    name = factory.Faker('word')
    description = factory.Faker('sentence')


class PriceFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания экземпляров модели Price"""

    class Meta:
        model = Price

    currency = factory.Iterator(['USD', 'EUR', 'RUB'])
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2,
                           positive=True)


class ProductFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания экземпляров модели Product"""
    class Meta:
        model = Product

    name = factory.Faker('word')
    price = factory.SubFactory(PriceFactory)
    quantity = factory.Faker('random_int', min=1, max=100)
    barcode = factory.Faker('ean13')
    type = factory.SubFactory(TypeFactory)
