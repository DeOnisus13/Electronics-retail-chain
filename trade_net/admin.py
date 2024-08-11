from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from trade_net.models import Contact, Product, RetailChain
from trade_net.services import clear_debt


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "date_of_launch", "seller",)
    search_fields = ("name",)
    list_filter = ("date_of_launch", "seller",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "seller", "country", "city", "street", "building",)
    search_fields = ("email",)
    list_filter = ("country", "city",)


clear_debt.short_description = _("Очистить задолженность")


@admin.register(RetailChain)
class NetworkChainAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", "get_supplier_chain", "debt",)
    search_fields = ("name", "supplier__name", "debt",)
    list_filter = ("name", "supplier",)
    actions = [clear_debt]
