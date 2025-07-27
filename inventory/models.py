import uuid
from django.db import models

# Table 1: Product master (prodmast)
class Product(models.Model):
    name = models.CharField(max_length=255)        # Name of the product
    sku = models.CharField(max_length=100, unique=True, default=uuid.uuid4)  # Stock Keeping Unit (unique identifier)
    description = models.TextField(blank=True)      # Optional description
    stock = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.name} ({self.sku})"

# Table 2: Stock transaction header (stckmain)
class StockTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Inward'),   # Stock came into warehouse
        ('OUT', 'Outward')  # Stock went out of warehouse
    )
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically store date/time

    def __str__(self):
        return f"{self.type} @ {self.timestamp}"

# Table 3: Stock transaction detail (stckdetail)
class StockDetail(models.Model):
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Can't be negative

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
