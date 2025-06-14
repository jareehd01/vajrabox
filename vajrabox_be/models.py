from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

class JewelryCategory(models.Model):
    """E.g., Rings, Necklaces, Bracelets"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name_plural = "Jewelry Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MetalType(models.Model):
    """Different metal options"""
    name = models.CharField(max_length=50)  # Gold, Silver, Platinum
    purity = models.CharField(max_length=20)  # 14K, 18K, 925 Sterling
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.purity})"

class Gemstone(models.Model):
    """Gemstone options for jewelry"""
    name = models.CharField(max_length=100)  # Diamond, Ruby, Sapphire
    color = models.CharField(max_length=50, blank=True)
    is_precious = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Core jewelry product model"""
    category = models.ForeignKey(JewelryCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    metal_type = models.ForeignKey(MetalType, on_delete=models.PROTECT)
    gemstones = models.ManyToManyField(Gemstone, through='ProductGemstone')
    weight_grams = models.DecimalField(max_digits=8, decimal_places=2)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    is_customizable = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    available_sizes = ArrayField(
        models.CharField(max_length=10),
        blank=True,
        default=list
    )  # For rings: ["6", "7", "8"]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.metal_type.name}")
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.base_price

    def __str__(self):
        return f"{self.name} ({self.metal_type.name})"

class ProductGemstone(models.Model):
    """Through model for gemstone details in products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gemstone = models.ForeignKey(Gemstone, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    size = models.CharField(max_length=20, blank=True)  # e.g., "0.5ct"
    placement = models.CharField(max_length=100, blank=True)  # e.g., "Center stone"

    class Meta:
        unique_together = [['product', 'gemstone', 'placement']]

class ProductImage(models.Model):
    """Multiple images per product with zoom capability"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary image exists
            ProductImage.objects.filter(
                product=self.product
            ).update(is_primary=False)
        super().save(*args, **kwargs)

class ProductVariant(models.Model):
    """For customizable jewelry options"""
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Engraving Option"
    price_modifier = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"{self.product.name} - {self.name}"