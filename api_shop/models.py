from django.db import models
from django.conf import settings
   

class OrdersChoices(models.TextChoices):
    NEW = 'N', 'NEW'
    PROGRESS  = 'P', 'PROGRESS'
    DONE = 'D', 'DONE'


class Order(models.Model):
    creator = models.ForeignKey(
      settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE,related_name='order_to_user')
    pozition_orders = models.ManyToManyField('Product', related_name = 'to_pozition', blank = True, through = 'OrderItem')
    status = models.TextField(choices=OrdersChoices.choices,default=OrdersChoices.NEW, verbose_name='Status')
    sum_order = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Summary',blank=True,null=True)
    created_at= models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    
    
    @property
    def total_price(self):
        return sum(item.sum_item for item in self.item.all())
    
    @property
    def total_item(self):
        return len(self.pozition_orders.all())

    def __str__(self):
        return f'{self.id}  {self.creator}  {self.status}'




class Product(models.Model):

    title = models.TextField(max_length=256, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(verbose_name='Price',max_digits=10, decimal_places=2)
    created_at= models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.id}  {self.title}'
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='item', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}  {self.order} - {self.product}   {self.quantity}'

    @property
    def sum_item(self):
        return self.quantity * self.product.price




class MarkChoices(models.TextChoices):
    
    ONE = 'ON', '1'
    TWO = 'TW', '2'
    THREE = 'TH', '3'
    FOUR = 'FR', '4'
    FIVE = 'FV', '5'


class Review(models.Model):
    creator = models.ForeignKey(
      settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE,related_name='review_to_user')
    product = models.ForeignKey(Product, related_name='review_about_product', on_delete = models.CASCADE)
    mark = models.TextField(choices=MarkChoices.choices, verbose_name='Rating')
    text = models.TextField(verbose_name='Review')
    created_at= models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


    def __str__(self):
        return f'{self.id} {self.creator} - {self.product} {self.mark}'


class Collection(models.Model):
    
    title = models.TextField(max_length=256, verbose_name='Title collection')
    description = models.TextField(verbose_name='Description')
    product = models.ManyToManyField(Product, related_name = 'collection', blank = True)
    created_at= models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return f'{self.id}  {self.title}'
    
    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
