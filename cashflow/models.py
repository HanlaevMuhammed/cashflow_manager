from django.db import models
from datetime import date
from django.utils import timezone



class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('type', 'name')

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    created_at = models.DateField(auto_now_add=True)
    date = models.DateField(null=True, blank=True)  # Дата может быть изменена вручную
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'
        ordering = ['-date', '-created_at']

    def save(self, *args, **kwargs):
        # При сохранении, если дата не указана, ставим сегодняшнюю
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.status} - {self.amount} руб."
