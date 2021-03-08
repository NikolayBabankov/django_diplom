from django.db import models
from django.conf import settings
from catalog.models import Product


class MarkChoices(models.TextChoices):
    ONE = 'ON', '1'
    TWO = 'TW', '2'
    THREE = 'TH', '3'
    FOUR = 'FR', '4'
    FIVE = 'FV', '5'


class Review(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='review_to_user')
    product = models.ForeignKey(
        Product, related_name='review_about_product', on_delete=models.CASCADE)
    mark = models.TextField(choices=MarkChoices.choices, verbose_name='Rating')
    text = models.TextField(verbose_name='Review')
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.id} {self.creator} - {self.product} {self.mark}'
