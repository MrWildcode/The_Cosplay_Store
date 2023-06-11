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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'
