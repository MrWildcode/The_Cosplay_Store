from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Products, UserProductRelation
from store.serializers import ProductsSerializer, UserProductRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend

from store.tests.permissions import IsOwnerOrStaffOrReadOnly


class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all().annotate(
        likes_count=Count(Case(When(userproductrelation__like=True, then=1)))).select_related(
        'owner').prefetch_related('watchers').order_by('id')

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


class UserProductRelationViewSet(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserProductRelation.objects.all()
    serializer_class = UserProductRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'product'

    def get_object(self):
        obj, _ = UserProductRelation.objects.get_or_create(user=self.request.user,
                                                           product_id=self.kwargs['product'])
        return obj
