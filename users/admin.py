from django.contrib import admin
from .models import CustomUser  # or your custom user model

admin.site.register(CustomUser)
