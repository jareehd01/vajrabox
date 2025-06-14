from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.JewelryCategoryViewSet)
router.register(r'metal-types', views.MetalTypeViewSet)
router.register(r'gemstones', views.GemstoneViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product-gemstones', views.ProductGemstoneViewSet)
router.register(r'product-images', views.ProductImageViewSet)
router.register(r'product-variants', views.ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]