from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug']
    
class sub_CategoryAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug']
    
class ProductAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug']    

class VariantAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Sub_Category,sub_CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variant,VariantAdmin)
admin.site.register(Main_Images)

admin.site.register(Cart)

