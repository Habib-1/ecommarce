from django.utils.text import slugify
from django.db import models
from common.models import BaseModel
from django.core.validators import MinValueValidator
# Create your models here.
class Category(BaseModel):
    name=models.CharField(max_length=150)
    slug=models.SlugField(max_length=180,unique=True,null=False,blank=False,db_index=True)
    description=models.TextField(null=True,blank=True)
    parent=models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",

    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ["name"]

    def __str__(self):
        return self.name

class Brand(BaseModel):
    name=models.CharField(max_length=150)
    slug=models.SlugField(max_length=200,unique=True,null=False,blank=False,)
    description=models.TextField(blank=True,null=True)
    logo=models.ImageField(upload_to="brands/",null=True,blank=True)


    class Meta:
        ordering = ["name"]
 

    def __str__(self):
        return self.name
    
class Product(BaseModel):
    name=models.CharField(max_length=150)
    slug=models.SlugField(max_length=200,unique=True,null=False,blank=False,)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(0)]
        )
    discount_price = models.DecimalField(max_digits=10, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
        )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name="products"
        )
    brand = models.ForeignKey(
        Brand, 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name="products"
        )
    sku = models.CharField(
        max_length=100, 
        unique=True, null=True, 
        blank=True,
        )
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ["-created_at"] 
        indexes = [
            models.Index(fields=["slug"]),  
            models.Index(fields=["sku"]),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return self.name

class Product_Image(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name} - Image"
    
