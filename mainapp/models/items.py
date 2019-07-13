from django.db import models
from .users import Buyer

'''
Тут создаю классы "правильной" модели создания юзеров в джанге...
'''


class Category(models.Model):
    """
    Класс описывающий категории товаров (например 'овощи'),
    связь один ко многим с таблицой Item
    """
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    mobile_id = models.IntegerField(default=0)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    color = models.TextField(null=True)

    class Meta:
        unique_together = ('buyer', 'name')


class Item(models.Model):
    """
    Класс описывающий товарs (например 'Чиспы')
    """
    mobile_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'name')

    def display_category(self):
        return self.category.name

    display_category.short_description = 'Name of category'