import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('sepatu', 'Sepatu'),
        ('jersey', 'Jersey'),
        ('celana', 'Celana'),
    ]
    
    name = models.CharField()
    price = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sepatu')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    