from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Products, UserProductRelation

class ProductWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProductsSerializer(ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    watchers = ProductWatcherSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'universe', 'owner', 'watchers', 'likes_count', 'rating')

    def get_likes_count(self, instance):
        return UserProductRelation.objects.filter(book=instance, like=True).count()

class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = 'product', 'like', 'in_cart', 'rate'
