from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from config.settings import NULLABLE


class RetailChain(models.Model):
    """Модель Поставщика"""

    LEVEL_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "ИП"),
    )

    name = models.CharField(max_length=150, verbose_name="Название")
    supplier = models.ForeignKey("self", on_delete=models.CASCADE, **NULLABLE, verbose_name="Поставщик")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень поставщика")
    debt = models.DecimalField(max_digits=30, decimal_places=2, default=0.00, verbose_name="Задолженность")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self) -> str:
        return f"{self.name}"

    def clean(self):
        """Валидация данных для модели поставщика"""

        """Запрет выбора самого себя в поле поставщик (supplier)"""
        if self.supplier and self.supplier == self:
            raise ValidationError("Нельзя выбрать в качестве поставщика самого себя")

        """Валидация уровня поставщика"""
        if self.supplier:
            if self.level == 0 and self.supplier.level != 0:
                raise ValidationError(
                    "Объект с уровнем 'Завод' не может иметь поставщика с уровнем 'Розничная сеть' или 'ИП'.")
            if self.level == 1 and self.supplier.level == 2:
                raise ValidationError("Объект с уровнем 'Розничная сеть' не может иметь поставщика с уровнем 'ИП'.")
            if self.level == 2 and self.supplier.level != 2:
                raise ValidationError("Объект с уровнем 'ИП' может быть поставщиком только для другого ИП.")

    def get_supplier_chain(self):
        """Возвращает цепочку поставщиков"""
        chain = []
        supplier = self.supplier
        while supplier:
            chain.append(supplier.name)
            supplier = supplier.supplier
        return " <- ".join(chain)

    get_supplier_chain.short_description = "Цепочка поставщиков"

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ("name",)


class Contact(models.Model):
    """Модель Контакта"""

    email = models.EmailField(max_length=50, verbose_name="Email")
    country = models.CharField(max_length=50, verbose_name="Страна")
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")
    building = models.CharField(max_length=10, verbose_name="Номер дома")
    seller = models.ForeignKey(RetailChain, on_delete=models.CASCADE, **NULLABLE, verbose_name="Продавец")

    def __str__(self) -> str:
        return f"{self.email} - {self.country} - {self.city}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ("city",)


class Product(models.Model):
    """Модель Продукта"""

    name = models.CharField(max_length=150, verbose_name="Название")
    model = models.CharField(max_length=50, **NULLABLE, verbose_name="Модель")
    date_of_launch = models.DateField(default=date.today, verbose_name="Дата выхода на рынок")
    seller = models.ForeignKey(RetailChain, on_delete=models.CASCADE, **NULLABLE, verbose_name="Продавец")

    def __str__(self) -> str:
        return f"{self.name} - {self.seller}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)
