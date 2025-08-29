from rest_framework import serializers
from .models import Category,Product,Brand,Product_Image

#============> Customer APIs Serializers <==========#
class CategorySerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField(read_only=True)
    parent=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []
    
    def get_parent(self,obj):
        if obj.parent:
            return obj.parent.name 
        return None

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields=['name','slug','description','logo',]
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # এখানে use_url=True দিলে URL আসবে

    class Meta:
        model = Product_Image
        fields = ["is_primary", "image"]


class ProductSerializer(serializers.ModelSerializer):
    category=serializers.SerializerMethodField()
    brand=serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model=Product
        fields=['name','slug','description','price','discount_price','stock','category','brand','sku','images']

    def get_category(self,obj):
        if obj.category:
            return obj.category.name
        return None
        
    def get_brand(self,obj):
        if obj.brand:
            return obj.brand.name
        return None
