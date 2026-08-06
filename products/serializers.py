from rest_framework import serializers
from .models import Category, Color,Product, ProductImage, Size

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image','order','is_primary']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            "size",
            "price",
            "discount_price",
            
        ]

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            "name",
            "image",
            
        ]

class ProductSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.name",allow_null=True)
    def get_primary_image(self,obj):
        image = obj.images.filter(is_primary=True).first()
        if not image :
            return None
        
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(image.image.url)
        return image.image.url
    class Meta:
        model = Product
        
        fields = [
            'name',
            'description',
            'slug',
            'price',
            'discount_price',
            'category',
            'primary_image',
            'is_available'
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name",allow_null=True)
    images = ProductImageSerializer(many=True)
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'slug',
            'price',
            'discount_price',
            'category',
            'images',
            'sizes',
            'colors'
        ]