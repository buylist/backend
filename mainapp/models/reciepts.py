from django.db import models
from .users import Buyer
from .items import Item


class Reciept(models.Model):
    """
    Таблица описывающая сущность Рецепт. Связана с пользоватлем (Byuer)
    """
    mobile_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'name')


class ItemInReciept(models.Model):
    """
    Таблица описывающая товары в рецепте
    """
    reciept = models.ForeignKey(
        Reciept, related_name='items_reciept', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.NullBooleanField(null=True, blank=True)
    value = models.DecimalField(
        verbose_name='стоимость выбранного количества',
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=0)
