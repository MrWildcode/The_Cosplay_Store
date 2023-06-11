from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from store.models import Products
from store.serializers import ProductsSerializer
from django_filters.rest_framework import DjangoFilterBackend

from store.tests.permissions import IsOwnerOrStaffOrReadOnly


class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['universe']
    search_fields = ['name', 'universe']
    ordering_fields = ['price', 'universe']

    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

def oauth(request):
    return render(request, 'oauth.html')




