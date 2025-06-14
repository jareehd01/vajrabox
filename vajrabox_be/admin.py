from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'metal_type', 'current_price', 'stock_quantity')
    list_filter = ('category', 'metal_type')
    search_fields = ('name', 'description')

admin.site.register([JewelryCategory, MetalType, Gemstone, ProductImage])