from django.db import models
from .users import Buyer
from .items import Item


class Checklist(models.Model):
    """
    Класс описывающий непосредственно сам список.
    Связан один ко многим с таблицей ItemInChecklist (Товары в списке)
    """
    mobile_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    share = models.CharField(blank=True, max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'name')


class ItemInChecklist(models.Model):
    """
    Класс -таблица содержащий в себе товары в списках.
    Связан с классом списков (Checklist)
    """
    checklist = models.ForeignKey(
        Checklist, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.NullBooleanField(null=True, blank=True)
    value = models.DecimalField(
        verbose_name='стоимость выбранного количества',
        max_digits=8, decimal_places=2,
        blank=True, default=0
    )

    def display_item(self):
        return self.item.name

    def display_checklist(self):
        return self.checklist.name

    display_checklist.short_description = 'Name of checklist'
    display_item.short_description = 'Name of item'


class ItemsInShared(models.Model):
    """
    Класс -таблица содержащий в себе товары в списках.
    Связан с классом списков (Checklist)
    """
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.NullBooleanField(null=True, blank=True)
    value = models.DecimalField(
        verbose_name='стоимость выбранного количества',
        max_digits=8, decimal_places=2,
        blank=True, default=0
    )
