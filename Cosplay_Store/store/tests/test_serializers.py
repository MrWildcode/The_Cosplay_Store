from rest_framework.test import APITestCase

from store.models import Products
from store.serializers import ProductsSerializer


class ProductsSerializerTestCase(APITestCase):
    def setUp(self):
        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars')
        self.product2 = Products.objects.create(name='testproduct2', price=800, universe='LOTR')

    def test_ok(self):
        data = ProductsSerializer([self.product1, self.product2], many=True).data
        expected_data = [
            {'id': self.product1.id,
             'name': 'testproduct1',
             'price': '500.00',
             'universe': 'Star Wars'},
            {'id': self.product2.id,
             'name': 'testproduct2',
             'price': '800.00',
             'universe': 'LOTR'},
            ]
        print(f'DATA {data}')
        print(f'EXPECTED_DATA {expected_data}')
        self.assertEqual(expected_data, data)