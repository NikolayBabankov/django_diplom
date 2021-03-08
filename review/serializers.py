from rest_framework import serializers
from django.contrib.auth.models import User
from review.models import Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class ReviewSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:

        model = Review
        fields = ('id', 'creator', 'product', 'mark', 'text', 'created_at')

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        review_item = Review.objects.filter(creator=validated_data['creator'])
        for item in review_item:
            if item.product == validated_data['product']:
                raise serializers.ValidationError(
                    {'product': 'There is already a review for this product'})
        return super().create(validated_data)
