from rest_framework import serializers
from .models import (
    JewelryCategory, MetalType, Gemstone, 
    Product, ProductGemstone, ProductImage, ProductVariant
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Customizing the JWT token payload
# to include additional user information
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        
        return token


class JewelryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JewelryCategory
        fields = '__all__'
        read_only_fields = ('slug',)

class MetalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalType
        fields = '__all__'

class GemstoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gemstone
        fields = '__all__'

class ProductGemstoneSerializer(serializers.ModelSerializer):
    gemstone = GemstoneSerializer(read_only=True)
    
    class Meta:
        model = ProductGemstone
        fields = ('gemstone', 'quantity', 'size', 'placement')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'is_primary', 'alt_text')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    metal_type = MetalTypeSerializer(read_only=True)
    gemstones = ProductGemstoneSerializer(
        source='productgemstone_set', 
        many=True, 
        read_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'metal_type', 'gemstones', 'weight_grams',
            'base_price', 'discount_price', 'current_price',
            'is_customizable', 'stock_quantity', 'available_sizes',
            'images', 'variants', 'created_at'
        ]
        read_only_fields = ('slug', 'created_at')