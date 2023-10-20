from django.db import models
import datetime
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from base.models import BaseModel
from Store.manager import UserProfileManager



# class Category(models.Model):
    
#     slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
#     name = models.CharField(max_length=150, null=False, blank=False)
#     image = models.ImageField(upload_to='category', null=True, blank=True )
#     description = models.TextField(max_length=500, null=False, blank=False)
#     status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
#     trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
#     meta_title = models.CharField(max_length=150, null=False, blank=False)
#     meta_keywords = models.CharField(max_length=150, null=False, blank=False)
#     meta_description = models.TextField(max_length=500, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug=slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)    
    
    # def __str__(self):
    #     return self.name
    
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')    
#     slug = models.SlugField(max_length=150, null=True, unique=True,blank=True)
#     name = models.CharField(max_length=150, null=False, blank=False)
#     product_image = models.ImageField(upload_to='product', null=True, blank=True )
#     small_description = models.CharField(max_length=250, null=False, blank=False)
#     quantity = models.IntegerField(null=False, blank=False) 
#     description = models.TextField(max_length=500, null=False, blank=False)
#     orginal_price = models.FloatField(null=False, blank=False)
#     selling_price = models.FloatField(null=False, blank=False)
#     status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
#     trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
#     tag = models.CharField(max_length=150, null=False, blank=False)
#     meta_title = models.CharField(max_length=150, null=False, blank=False)
#     meta_keywords = models.CharField(max_length=150, null=False, blank=False)
#     meta_description = models.TextField(max_length=500, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug=slugify(self.name)
#         super(Product, self).save(*args, **kwargs)    
    
   
    
#     def __str__(self):
#         return self.name





class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def _str_(self):
        return self.email

    def get_full_name(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.email)
        super(UserProfile, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    

    


class Category(BaseModel):
    
    name = models.CharField(max_length=150, )
    image = models.ImageField(upload_to='category/', null=True, blank=True )
    description = models.TextField(max_length=500, null=False, blank=False)
    
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Category, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    

class Sub_Category(BaseModel):
    
    name = models.CharField(max_length=150, unique=True)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="sub_categories")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Sub_Category, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    
class Product(BaseModel):
          
    description = models.TextField(max_length=500) 
    sub_category_id = models.ForeignKey(Sub_Category,on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    

class Variant(BaseModel):
    SIZE_CHOICES = [
        ('500ml', '500ml'),
        ('1000ml', '1000ml'),
    ]
    
    
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    orginal_price = models.FloatField()
    selling_price = models.FloatField()
    quantity = models.IntegerField()
    cover_image = models.ImageField(upload_to='product/' )
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color =models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.color)
        super(Variant, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.color
    
   
 
 
class Cart(BaseModel):
    pass
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product_qty = models.IntegerField(null=False, blank=False)
    # created_at = models.DateTimeField(auto_now_add=True)
  