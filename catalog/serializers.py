from rest_framework import serializers
from catalog.models import Product, Collection


class ProductSerializer(serializers.ModelSerializer):

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError(
                'The price cannot be zero or negative')
        return price

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price')


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ('id', 'title', 'description', 'product')

    def validate_product(self, product):
        if product == []:
            raise serializers.ValidationError(
                'You cannot create a collection without products')
        return product

    def create(self, validated_data):
        collection = Collection.objects.create(
            title=validated_data['title'],
            description=validated_data['description']
        )
        for prod in validated_data['product']:
            product = Product.objects.get(id=prod.id)
            collection.product.add(product)
        collection.save()

        return collection
