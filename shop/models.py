from django.db import models
from common.models import BaseModel
# Create your models here.
class ShopInfo(BaseModel):
    shop_name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logo/')
  

    def __str__(self):
        return self.shop_name