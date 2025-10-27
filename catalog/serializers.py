from rest_framework import serializers
from .models import Category,Product,Brand,Product_Image,Slider,Variant,Size,Color

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

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name','hex_code']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class VariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    class Meta:
        model = Variant
        fields = ['id', 'color', 'size', 'price', 'stock','color','size',]


class ProductSerializer(serializers.ModelSerializer):
    category=serializers.SerializerMethodField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    brand=serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    class Meta:
        model=Product
        fields=['id','name','slug','description','price','discount_price','stock','category','category_slug','brand','sku','images','variants']

    def get_category(self,obj):
        if obj.category:
            return obj.category.name
        return None
        
    def get_brand(self,obj):
        if obj.brand:
            return obj.brand.name
        return None




class SliderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Slider
        fields = ['id', 'image', 'alt', 'is_active']
