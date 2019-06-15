from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy


class Buyer(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.SlugField(gettext_lazy('username'), unique=True, validators=[username_validator], max_length=50,
                                error_messages={
                                    'unique': gettext_lazy('A user with that username already exists'),
                                }, )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Category(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Checklist(models.Model):
    checklist_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Item(models.Model):
    item_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class ItemInChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
