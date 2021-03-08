from django.db import models


class Product(models.Model):
    title = models.TextField(max_length=256, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(
        verbose_name='Price', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title}'


class Collection(models.Model):
    title = models.TextField(max_length=256, verbose_name='Title collection')
    description = models.TextField(verbose_name='Description')
    product = models.ManyToManyField(
        Product, related_name='collection', blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.id}  {self.title}'

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
