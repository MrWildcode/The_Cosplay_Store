import json

from django.contrib.auth.models import User
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Products, UserProductRelation
from store.serializers import ProductsSerializer


class ProductsAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username='testuser3', is_staff=True)

        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars',
                                                owner=self.user1)
        self.product2 = Products.objects.create(name='testproduct2', price=900, universe='LOTR',
                                                owner=self.user1)
        self.product3 = Products.objects.create(name='Something from Star Wars', price=800, universe='Other',
                                                owner=self.user2)

        UserProductRelation.objects.create(user=self.user1, product=self.product3, like=True, rate=4)

    def test_get(self):
        url = reverse('products-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
        products = Products.objects.all().annotate(
        likes_count=Count(Case(When(userproductrelation__like=True, then=1))),
        rating=Avg('userproductrelation__rate')).order_by('id')
        expected_data = ProductsSerializer(products, many=True).data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data[2]['likes_count'], 1)
        self.assertEqual(expected_data[2]['rating'], '4.00')

    def test_get_filter(self):
        url = reverse('products-list')
        response = self.client.get(url, data={'universe': 'LOTR'})
        products = Products.objects.filter(id__in=[self.product2.id]).annotate(
            likes_count=Count(Case(When(userproductrelation__like=True, then=1))),
            rating=Avg('userproductrelation__rate')).order_by('id')
        expected_data = ProductsSerializer(products, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_search(self):
        url = reverse('products-list')
        response = self.client.get(url, data={'search': 'Star Wars'})
        products = Products.objects.filter(id__in=[self.product1.id, self.product3.id]).annotate(
            likes_count=Count(Case(When(userproductrelation__like=True, then=1))),
            rating=Avg('userproductrelation__rate')).order_by('id')
        expected_data = ProductsSerializer(products, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_ordering(self):
        url = reverse('products-list')
        response = self.client.get(url, data={'ordering': 'price'})
        products = Products.objects.all().annotate(
            likes_count=Count(Case(When(userproductrelation__like=True, then=1))),
            rating=Avg('userproductrelation__rate')).order_by('price')
        expected_data = ProductsSerializer(products, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create(self):
        url = reverse('products-list')
        data = {'name': 'testproduct4',
                'price': '350',
                'universe': 'Resident Evil'}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.last().owner, self.user1)

    def test_update(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {'name': self.product1.name,
                'price': '650.00',
                'universe': self.product1.universe}
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(data['price'], str(self.product1.price))

    def test_update_not_authenticated(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {'name': self.product1.name,
                'price': '650.00',
                'universe': self.product1.universe}
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product1.refresh_from_db()
        self.assertEqual(Products.objects.get(id=self.product1.id).price, self.product1.price)

    def test_update_not_owner(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {'name': self.product1.name,
                'price': '650.00',
                'universe': self.product1.universe}
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product1.refresh_from_db()
        self.assertEqual(Products.objects.get(id=self.product1.id).price, self.product1.price)

    def test_update_not_owner_but_staff(self):
        url = reverse('products-detail', args=(self.product1.id,))
        data = {'name': self.product1.name,
                'price': '650.00',
                'universe': self.product1.universe}
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.put(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(data['price'], str(self.product1.price))

    def test_delete(self):
        url = reverse('products-detail', args=(self.product2.id,))
        self.assertTrue(Products.objects.get(id=self.product2.id))
        self.assertEqual(3, Products.objects.count())
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Products.objects.count())


class ProductRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')

        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars')
        self.product2 = Products.objects.create(name='testproduct2', price=900, universe='LOTR')

    def test_like(self):
        url = reverse('userproductrelation-detail', args=(self.product1.id,))
        data = {
            'like': True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relation_updated = UserProductRelation.objects.get(user=self.user1, product=self.product1)
        self.assertTrue(relation_updated.like)

    def in_cart(self):
        url = reverse('userproductrelation-detail', args=(self.product1.id,))
        data = {
            'in_cart': True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserProductRelation.objects.get(user=self.user1,
                                                        product=self.product1).in_cart)

    def test_rate(self):
        url = reverse('userproductrelation-detail', args=(self.product2.id,))
        data = {
            'rate': 4
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.patch(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserProductRelation.objects.get(user=self.user2,
                                                        product=self.product2).rate)