from django.db import models
from users.models import CustomUser

class LostItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    lost_date = models.DateField()
    lost_location = models.CharField(max_length=255)  # Manual location input
    latitude = models.FloatField(null=True, blank=True)  # Map-selected latitude
    longitude = models.FloatField(null=True, blank=True)  # Map-selected longitude
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name
