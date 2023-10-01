from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Добавьте поля для продавца


class AuctionParticipant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Добавьте поля для участника аукциона


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
