import django_filters
from django_filters.rest_framework import FilterSet

from trade_net.models import RetailChain


def clear_debt(modeladmin, request, queryset):
    """Функция обнуления задолженности выбранных поставщиков"""
    queryset.update(debt=0.00)
    return queryset


class CountryFilter(FilterSet):
    """Фильтр по стране контакта"""

    country = django_filters.CharFilter(field_name="contact__country", lookup_expr="icontains")

    class Meta:
        model = RetailChain
        fields = ["country"]
