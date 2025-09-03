from django.db import models
from common.models import BaseModel
from catalog.models import Product
from accounts.models import Customer

# Create your models here.
class Cart(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="carts")
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} for {self.customer.user.email}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
    




    

class Wishlist(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlists")


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)