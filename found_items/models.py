from django.db import models
from users.models import CustomUser
from lost_items.models import LostItem


class FoundItem(models.Model):
    CATEGORY_CHOICES = LostItem.CATEGORY_CHOICES  

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    found_date = models.DateField()
    found_location = models.CharField(max_length=255)  # for human-readable name or area
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='found_items/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name
