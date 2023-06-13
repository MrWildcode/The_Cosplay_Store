from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from store.models import Products, UserProductRelation
from store.rating_logic import set_rating


class SetRatingTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        self.user2 = User.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        self.user3 = User.objects.create(username='test_username3', first_name='1', last_name='2')

        self.product1 = Products.objects.create(name='testproduct1', price=500, universe='Star Wars',
                                                    owner=self.user1)

        UserProductRelation.objects.create(user=self.user1, product=self.product1, like=True, rate=3)
        UserProductRelation.objects.create(user=self.user2, product=self.product1, like=True, rate=4)
        UserProductRelation.objects.create(user=self.user3, product=self.product1, like=True)

    def test_ok(self):
        set_rating(self.product1)
        self.product1.refresh_from_db()
        self.assertEqual(str(self.product1.rating), '3.50')

