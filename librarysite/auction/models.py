from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    limit_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_date = models.DateTimeField()

    def __str__(self):
        return self.name
