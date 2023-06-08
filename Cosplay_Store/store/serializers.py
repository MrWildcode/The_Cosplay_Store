from rest_framework.serializers import ModelSerializer

from store.models import Products


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'