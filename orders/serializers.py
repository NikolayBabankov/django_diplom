from rest_framework import serializers
from django.contrib.auth.models import User
from orders.models import Order, OrderItem


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):

    item = OrderItemSerializer(
        many=True,
        required=True,
    )
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ('id', 'creator', 'status', 'sum_order', 'item')

    def validate_item(self, item):
        item_ids = [it['product'].id for it in item]

        if item_ids == []:
            raise serializers.ValidationError(
                'The order does not contain any products')
        item_ids_set = set(item_ids)

        if len(item_ids_set) != len(item):
            raise serializers.ValidationError(
                'There are duplicates in the order')

        return item

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        item_data = validated_data.pop('item')
        order = super().create(validated_data)

        raw_item = []

        for item_data in item_data:
            items = OrderItem(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
            )

            raw_item.append(items)

        OrderItem.objects.bulk_create(raw_item)
        order.sum_order = order.total_price
        order.save()
        return order

    def update(self, instance, validated_data):
        if validated_data.get('status') is not None:
            if self.context['request'].user.is_superuser:
                instance.status = validated_data.get('status', instance.status)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError(
                    'Only the admin can change status')

        item_data = validated_data.pop('item')
        raw_item = []

        for item_data in item_data:
            items = OrderItem(
                order=instance,
                product=item_data['product'],
                quantity=item_data['quantity'],
            )

            raw_item.append(items)
        OrderItem.objects.filter(order=instance).delete()
        OrderItem.objects.bulk_create(raw_item)
        instance.sum_order = instance.total_price
        instance.save()
        return instance
