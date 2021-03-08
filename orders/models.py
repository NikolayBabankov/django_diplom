from django.db import models
from django.conf import settings
from catalog.models import Product


class OrdersChoices(models.TextChoices):
    NEW = 'N', 'NEW'
    PROGRESS = 'P', 'PROGRESS'
    DONE = 'D', 'DONE'


class Order(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='order_to_user')
    position_orders = models.ManyToManyField(
        Product, related_name='to_position', blank=True, through='OrderItem')
    status = models.TextField(
        choices=OrdersChoices.choices,
        default=OrdersChoices.NEW, verbose_name='Status')
    sum_order = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Summary', blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def total_price(self):
        return sum(item.sum_item for item in self.item.all())

    @property
    def total_item(self):
        return len(self.position_orders.all())

    def __str__(self):
        return f'{self.id}  {self.creator}  {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='item', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}  {self.order} - {self.product}   {self.quantity}'

    @property
    def sum_item(self):
        return self.quantity * self.product.price
