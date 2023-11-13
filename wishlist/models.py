from django.db import models
import uuid
from Store.models import *

# Create your models here.

class WishlistModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='wishlist_item')
    
    def __str__(self):
        return f"wishlist for {self.user.username}"
