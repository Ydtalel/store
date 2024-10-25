import pytest
from django.urls import reverse
from rest_framework import status

from store_app.models import Product
from store_app.tests.factories import (TypeFactory, PriceFactory,
                                       ProductFactory)


@pytest.mark.django_db
class TestProductAPI:
    """Тесты для CRUD операций и метода уменьшения количества товара через
    API
    """

    def test_create_product(self, api_client):
        """Тест создания товара через API"""
        type_instance = TypeFactory()
        price_instance = PriceFactory()

        url = reverse('product-list')
        data = {
            "name": "Laptop",
            "price": price_instance.id,
            "quantity": 20,
            "barcode": "0987654321",
            "type": type_instance.id,
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        assert Product.objects.get().name == "Laptop"

    def test_get_products(self, api_client):
        """Тест получения списка товаров через API"""
        product = ProductFactory()

        url = reverse('product-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == product.name

    def test_update_product(self, api_client):
        """Тест обновления товара через API"""
        product = ProductFactory()

        url = reverse('product-detail', args=[product.id])
        data = {
            "name": "Updated Laptop",
            "price": product.price.id,
            "quantity": 50,
            "barcode": product.barcode,
            "type": product.type.id,
        }
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.name == "Updated Laptop"
        assert product.quantity == 50

    def test_delete_product(self, api_client):
        """Тест удаления товара через API"""
        product = ProductFactory()

        url = reverse('product-detail', args=[product.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0

    def test_reduce_quantity(self, api_client):
        """Тест уменьшения количества товара через API"""
        product = ProductFactory(quantity=50)

        url = reverse('product-reduce-quantity', args=[product.id])
        data = {"quantity": 10}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.quantity == 40  # 50 - 10 = 40

    def test_not_enough_quantity(self, api_client):
        """Тест уменьшения количества товара с недостаточным количеством"""
        product = ProductFactory(quantity=50)

        url = reverse('product-reduce-quantity', args=[product.id])
        data = {"quantity": 60}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Not enough value to reduce" in response.data["error"]
