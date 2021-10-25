from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class PersonalInfos(models.Model): 
    user = models.ForeignKey(User, related_name="infos", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    instagram = models.URLField(max_length=200, default="")
    instagram_followers = models.IntegerField(default=0)
    facebook = models.URLField(max_length=200, default="")
    facebook_followers = models.IntegerField(default=0)
    tiktok = models.URLField(max_length=200, default="")
    tiktok_followers = models.IntegerField(default=0)
    youtube = models.URLField(max_length=200, default="")
    youtube_followers = models.IntegerField(default=0)


class Order(models.Model):
    name = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "%s" % self.id
