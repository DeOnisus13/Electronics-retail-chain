from rest_framework.routers import DefaultRouter

from trade_net.apps import TradeNetConfig
from trade_net.views import ContactViewSet, ProductViewSet, RetailChainViewSet

app_name = TradeNetConfig.name

retail_router = DefaultRouter()
retail_router.register(r"retail", RetailChainViewSet, basename="retail")

product_router = DefaultRouter()
product_router.register(r"product", ProductViewSet, basename="product")

contact_router = DefaultRouter()
contact_router.register(r"contact", ContactViewSet, basename="contact")


urlpatterns = [] + retail_router.urls + product_router.urls + contact_router.urls
