from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Type, Price
from .serializers import ProductSerializer, TypeSerializer, PriceSerializer


class TypeViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к модели Type"""

    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class PriceViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к модели Price"""

    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к модели Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], url_path='reduce-quantity')
    def reduce_quantity(self, request, pk=None):
        """Уменьшает количество продукта на заданное значение"""
        product = self.get_object()
        try:
            reduce_by = int(request.data.get('quantity', 0))
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid quantity value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reduce_by <= 0:
            return Response(
                {"error": "Quantity should be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product.quantity < reduce_by:
            return Response(
                {"error": "Not enough value to reduce"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.quantity -= reduce_by
        product.save()
        return Response(
            {"success": f"Reduced quantity by {reduce_by}."
                        f" Remaining: {product.quantity}"},
            status=status.HTTP_200_OK
        )
