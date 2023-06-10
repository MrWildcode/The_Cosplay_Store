import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Products
from store.serializers import ProductsSerializer


class ProductsAPITestCase(APITestCase):
    def setUp(self):
        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars')
        self.product2 = Products.objects.create(name='testproduct2', price=800, universe='LOTR')
        self.product3 = Products.objects.create(name='Something from Star Wars', price=800, universe='Other')

    def test_get(self):
        url = reverse('products-list')
        response = self.client.get(url)
        expected_data = ProductsSerializer([self.product1, self.product2, self.product3], many=True).data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_filter(self):
        url = reverse('products-list')
        response = self.client.get(url, data={'universe': 'LOTR'})
        expected_data = ProductsSerializer([self.product2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_search(self):
        url = reverse('products-list')
        response = self.client.get(url, data={'search': 'Star Wars'})
        expected_data = ProductsSerializer([self.product1, self.product3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create(self):
        url = reverse('products-list')
        data = {'name': 'testproduct4',
                'price': '350',
                'universe': 'Resident Evil'}
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {'name': self.product1.name,
                'price': '650.00',
                'universe': self.product1.universe}
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(data['price'], str(self.product1.price))

    def test_delete(self):
        url = reverse('products-detail', args=(self.product2))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, Products.objects.count())



