from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from store.models import Products
from store.serializers import ProductsSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['universe']
    search_fields = ['name', 'universe']
    ordering_fields = ['price', 'universe']



