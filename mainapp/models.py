from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy


'''
Тут создаю классы "правильной" модели создания юзеров в джанге...
'''


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Buyer(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    username_validator = UnicodeUsernameValidator()
    username = models.SlugField(gettext_lazy('username'), unique=True, validators=[username_validator], max_length=50,
                                error_messages={
                                    'unique': gettext_lazy('A user with that username already exists'),
                                }, )


class Category(models.Model):
    mobile_category_id = models.IntegerField(default=0)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    color = models.TextField(null=True)

    class Meta:
        unique_together = ('buyer', 'name')


class Checklist(models.Model):
    checklist_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'name')


class Item(models.Model):
    item_id = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('buyer', 'name')  # Задаем уникальное сочетание для двух столбцов


class ItemInChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='item_info', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.NullBooleanField(null=True, blank=True)
    value = models.DecimalField(verbose_name='стоимость выбранного количества', max_digits=8, decimal_places=2,
                                blank=True, default=0)

    def display_item(self):
        return self.item.name

    display_item.short_description = 'Name of item'


class FromWebProdFields(models.Model):
    prod_name = models.CharField(verbose_name='название товара', max_length=128)
    web_prod_name = models.CharField(verbose_name='название товара в каталогах сайтов', max_length=128, blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, blank=False)
    measure = models.CharField(verbose_name='измерение', max_length=2, blank=True)
    volume = models.CharField(verbose_name='объем упаковки', max_length=2, blank=True)
    picture = models.CharField(verbose_name='адрес_фотографии', max_length=256, blank=True)
    source = models.CharField(verbose_name='источник данных', max_length=256, blank=True)