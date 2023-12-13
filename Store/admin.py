from django.contrib import admin
from .models import *
from .forms import *

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
    exclude = ['slug',]
    
    
class ColorImageAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug',]     
    
    
class UserAdmin(admin.ModelAdmin):
    list_display=['id','username','email', 'profile_image', 'is_active','is_superuser']
    search_fields=['email','username']
    readonly_fields=['last_login','password']
    list_filter=['last_login']
    list_editable=('is_active',)
 
 
class UserdpAdmin(admin.ModelAdmin):
    # list_display = []  
    exclude = ['slug']       

class PeromoCodeAdmin(admin.ModelAdmin):
    form = PeromoCodeForm
    list_display=['code','discount_price','purchase_price','expaire_date',]

class OrderAdmin(admin.ModelAdmin):
    inlines = []
  
class OrderItemAdmin(admin.ModelAdmin):
    form = PeromoCodeForm
    list_display=[]
    


admin.site.register(Category,CategoryAdmin)
admin.site.register(Sub_Category,sub_CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variant,VariantAdmin)
admin.site.register(Main_Images)
admin.site.register(Logo)
admin.site.register(UserProfile,UserAdmin)
admin.site.register(ColorImage,ColorImageAdmin)
admin.site.register(Userdp,UserdpAdmin)
admin.site.register(PeromoCode,PeromoCodeAdmin)



admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)




