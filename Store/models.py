from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import UserManager
import datetime
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from base.models import BaseModel
from Store.manager import UserProfileManager



class Main_Images(BaseModel):
    cover_image = models.ImageField(upload_to='main_img/' )
    
    
class Logo(BaseModel):
    cover_image = models.ImageField(upload_to='Logo_img/' )
   

class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True, editable=True)
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
        return self.username
 
 
 
 
class CustomUserManager(UserManager):
     def _create_user(self, email, password, **extra_fields):
         if not email:
             raise ValueError("You have not provided a valid email")
         
    
            

    


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
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="sub_categories")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Sub_Category, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    
class Product(BaseModel):
          
    description = models.TextField(max_length=500) 
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE, related_name="products")
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
    
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
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
  
  
  



# category
class Categoryy(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/") 
    
    def __str__(self):
        return self.title 
    
  
# brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/") 
    
    def __str__(self):
        return self.title 
      
  
# color
class Colorr(models.Model):
    title=models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title  
    
#size    
class Sizee(models.Model):
    title=models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.title  
    
#productmodel    
class Productt(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="product_imgs/") 
    slug=models.CharField(max_length=100)
    detail=models.TextField()
    specs=models.TextField()
    price=models.PositiveIntegerField()
    categoryy=models.ForeignKey(Categoryy,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    colorr=models.ForeignKey(Colorr,on_delete=models.CASCADE)
    sizee=models.ForeignKey(Sizee,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    


#product Attribute

class ProductAttribute(models.Model):
    productt=models.ForeignKey(Productt,on_delete=models.CASCADE)
    colorr=models.ForeignKey(Colorr,on_delete=models.CASCADE) 
    sizee=models.ForeignKey(Sizee,on_delete=models.CASCADE) 
    price=models.PositiveIntegerField()
    
    def __str__(self):
        return self.productt.title
    
    
    
    
             