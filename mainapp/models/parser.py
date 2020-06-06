from django.db import models


class FromWebProdFields(models.Model):
    """
    Модель данных собираемых парсером
    """
    prod_name = models.CharField(verbose_name='название товара', max_length=128)
    web_prod_name = models.CharField(verbose_name='название товара в каталогах сайтов', max_length=128, blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, blank=False)
    measure = models.CharField(verbose_name='измерение', max_length=4, blank=True)
    volume = models.CharField(verbose_name='объем упаковки', max_length=10, blank=True)
    picture = models.CharField(verbose_name='адрес_фотографии', max_length=256, blank=True)
    source = models.CharField(verbose_name='источник данных', max_length=256, blank=True)
