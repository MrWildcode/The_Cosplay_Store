from django.contrib.auth.models import User
from django.db import models

class Products(models.Model):
    UNIVERSE_CHOICES = (
        ('Star Wars', 'Star Wars'),
        ('Resident Evil', 'Resident Evil'),
        ('LOTR', 'Lord Of The Rings'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    universe = models.CharField(choices=UNIVERSE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='my_products')
    watchers = models.ManyToManyField(User, through='UserProductRelation',
                                      related_name='products')

    def __str__(self):
        return f'ID {self.id}: {self.name}'

class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Terrible'),
        (2, 'Bad'),
        (3, 'Ok'),
        (4, 'Good'),
        (5, 'Perfect'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    like = models.BooleanField(default=False)
    in_cart = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.product.name}, RATE {self.rate}'
