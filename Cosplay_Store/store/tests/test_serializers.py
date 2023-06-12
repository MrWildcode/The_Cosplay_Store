from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from store.models import Products
from store.serializers import ProductsSerializer


class ProductsSerializerTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars', owner=self.user1)
        self.product2 = Products.objects.create(name='testproduct2', price=800, universe='LOTR', owner=self.user1)

    def test_ok(self):
        data = ProductsSerializer([self.product1, self.product2], many=True).data
        expected_data = [
            {'id': self.product1.id,
             'name': 'testproduct1',
             'price': '500.00',
             'universe': 'Star Wars',
             'owner': self.user1.id,
             'watchers': []},
            {'id': self.product2.id,
             'name': 'testproduct2',
             'price': '800.00',
             'universe': 'LOTR',
             'owner': self.user1.id,
             'watchers': []},
            ]
        print(f'EXPECTED DATA {expected_data}')
        print(f'DATA {data}')
        self.assertEqual(expected_data, data)