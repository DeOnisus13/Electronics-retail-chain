from rest_framework import serializers

from trade_net.models import Contact, Product, RetailChain


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для модели контактов"""

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели продуктов"""

    class Meta:
        model = Product
        fields = "__all__"


class RetailChainSerializer(serializers.ModelSerializer):
    """Сериализатор для модели поставщиков"""

    contacts = ContactSerializer(source="contact_set", many=True, read_only=True)
    products = ProductSerializer(source="product_set", many=True, read_only=True)
    supplier_chain = serializers.SerializerMethodField()

    def get_supplier_chain(self, obj):
        return obj.get_supplier_chain()

    def update(self, instance, validated_data):
        """Запрет изменения поля "задолженность (debt) при обновлении через API-запрос"""
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)

    class Meta:
        model = RetailChain
        fields = "__all__"
