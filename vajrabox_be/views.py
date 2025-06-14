from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    JewelryCategory, MetalType, Gemstone,
    Product, ProductGemstone, ProductImage, ProductVariant
)
from .serializers import (
    CustomTokenObtainPairSerializer, JewelryCategorySerializer, MetalTypeSerializer,
    GemstoneSerializer, ProductSerializer,
    ProductGemstoneSerializer, ProductImageSerializer,
    ProductVariantSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class JewelryCategoryViewSet(viewsets.ModelViewSet):
    queryset = JewelryCategory.objects.all()
    serializer_class = JewelryCategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class MetalTypeViewSet(viewsets.ModelViewSet):
    queryset = MetalType.objects.all()
    serializer_class = MetalTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'purity']

class GemstoneViewSet(viewsets.ModelViewSet):
    queryset = Gemstone.objects.all()
    serializer_class = GemstoneSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'color']
    filterset_fields = ['is_precious']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        'metal_type', 'category'
    ).prefetch_related(
        'productgemstone_set__gemstone',
        'images',
        'variants'
    ).all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'metal_type__name']
    filterset_fields = {
        'category': ['exact'],
        'metal_type': ['exact'],
        'base_price': ['gte', 'lte'],
        'is_customizable': ['exact'],
    }

class ProductGemstoneViewSet(viewsets.ModelViewSet):
    queryset = ProductGemstone.objects.select_related(
        'product', 'gemstone'
    ).all()
    serializer_class = ProductGemstoneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'gemstone']

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'is_primary']

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']