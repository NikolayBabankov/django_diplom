from rest_framework import serializers
from django.contrib.auth.models import User
from api_shop.models import Order,OrderItem,Product,Review,Collection

class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для пользователя'''

    class Meta:
        model = User
        fields = ('id', 'username')

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields=("id","product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    '''Сериализатор для заказов'''

    item = OrderItemSerializer(
        many = True,
        required=True,
    )
    creator = UserSerializer(
        read_only=True,
    )


    class Meta:
        model=Order
        fields = ("id", "creator","status","sum_order","item")

    def validate_item(self, item):
        item_ids = [it['product'].id for it in item]
        
        if item_ids == []:
            raise serializers.ValidationError('The order does not contain any products')
        item_ids_set = set(item_ids)
        
        if len(item_ids_set) != len(item):
            raise serializers.ValidationError('Contains duplicate positions')

        return item


    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        item_data = validated_data.pop("item")
        order = super().create(validated_data)

        raw_item = []

        for item_data in item_data:
            items = OrderItem(
                order = order,
                product= item_data["product"],
                quantity= item_data["quantity"],
            )

            raw_item.append(items)
    

        OrderItem.objects.bulk_create(raw_item)
        order.sum_order = order.total_price
        order.save()
        return order

    def update(self, instance,validated_data):
        if self.context["request"].user.is_superuser:
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance
        
        item_data = validated_data.pop("item")
        raw_item = []

        for item_data in item_data:
            items = OrderItem(
                order = instance,
                product= item_data["product"],
                quantity= item_data["quantity"],
            )

            raw_item.append(items)
        OrderItem.objects.filter(order=instance).delete()
        OrderItem.objects.bulk_create(raw_item)
        instance.sum_order = instance.total_price
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    '''Сериализатор для товаров'''

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('The price cannot be zero or negative')
        return price

    class Meta:
        model=Product
        fields = ("id", "title","description","price")


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для отзывов'''

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:

        model = Review
        fields = ("id", "creator","product", "mark", "text","created_at")
    
    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        review_item = Review.objects.filter(creator= validated_data["creator"])
        for item in review_item:
            if item.product == validated_data["product"]:
                raise serializers.ValidationError({'product':'There is already a review for this product'})
        return super().create(validated_data)

    
class CollectionSerializer(serializers.ModelSerializer):
    '''Сериализатор для коллекций'''    

    class Meta:
        model = Collection
        fields=("id","title","description", "product")
    

    def validate_product(self, product):
        if product == []:
            raise serializers.ValidationError('You cannot create a collection without products')     
        return product
    

    def create(self, validated_data):

        collection = Collection.objects.create(
            title = validated_data['title'],
            description = validated_data['description']
        )
        for prod in validated_data['product']:
            product = Product.objects.get(id = prod.id)
            collection.product.add(product)
        collection.save()

        return collection
