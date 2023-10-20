from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        abstract = True