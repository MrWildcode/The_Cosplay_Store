from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from rest_framework.test import APITestCase

from store.models import Products, UserProductRelation
from store.serializers import ProductsSerializer


class ProductsSerializerTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        self.user2 = User.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        self.user3 = User.objects.create(username='test_username3', first_name='1', last_name='2')

        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars', owner=self.user1)
        self.product2 = Products.objects.create(name='testproduct2', price=800, universe='LOTR', owner=self.user1)

        UserProductRelation.objects.create(user=self.user1, product = self.product1, like=True, rate=3)
        UserProductRelation.objects.create(user=self.user2, product=self.product1, like=True, rate=4)
        UserProductRelation.objects.create(user=self.user3, product=self.product1, like=True)

        UserProductRelation.objects.create(user=self.user1, product = self.product2, like=True)
        UserProductRelation.objects.create(user=self.user2, product=self.product2, like=True, rate=2)
        UserProductRelation.objects.create(user=self.user3, product=self.product2, like=False, rate=4)
    def test_ok(self):
        products = Products.objects.all().annotate(
        likes_count=Count(Case(When(userproductrelation__like=True, then=1))),
        rating=Avg('userproductrelation__rate')).order_by('id')
        data = ProductsSerializer(products, many=True).data
        expected_data = [
            {'id': self.product1.id,
             'name': 'testproduct1',
             'price': '500.00',
             'universe': 'Star Wars',
             'owner': self.user1.id,
             'watchers': [
                 {
                     'first_name': 'Ivan',
                     'last_name': 'Petrov'
                 },
                 {
                     'first_name': 'Ivan',
                     'last_name': 'Sidorov'
                 },
                 {
                     'first_name': '1',
                     'last_name': '2'
                 },
             ],
             'likes_count': 3,
             'rating': '3.50'},
            {'id': self.product2.id,
             'name': 'testproduct2',
             'price': '800.00',
             'universe': 'LOTR',
             'owner': self.user1.id,
             'watchers': [
                 {
                     'first_name': 'Ivan',
                     'last_name': 'Petrov'
                 },
                 {
                     'first_name': 'Ivan',
                     'last_name': 'Sidorov'
                 },
                 {
                     'first_name': '1',
                     'last_name': '2'
                 },
             ],
             'likes_count': 2,
             'rating': '3.00'},
            ]
        self.assertEqual(expected_data, data)