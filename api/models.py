from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)