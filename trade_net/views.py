from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from trade_net.models import Contact, Product, RetailChain
from trade_net.serializers import (ContactSerializer, ProductSerializer,
                                   RetailChainSerializer)
from trade_net.services import CountryFilter
from users.permissions import IsActiveStaff


class ProductViewSet(viewsets.ModelViewSet):
    """Контроллер CRUD для работы с продуктами"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActiveStaff,)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ContactViewSet(viewsets.ModelViewSet):
    """Контроллер CRUD для работы с контактами"""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsActiveStaff,)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RetailChainViewSet(viewsets.ModelViewSet):
    """Контроллер CRUD для работы с поставщиками"""

    queryset = RetailChain.objects.all().order_by("id")
    serializer_class = RetailChainSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter
    permission_classes = (IsActiveStaff,)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
