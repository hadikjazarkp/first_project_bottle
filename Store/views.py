from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required




def home(request):
    print(request.user.username)
    main_images = Main_Images.objects.first()
    category = Category.objects.all()
    product = Product.objects.all()
    # variant = Variant.objects.all()
    
    return render(request,"store/index.html", {'main_images': main_images, 'category': category, 'product':product})



def my_view(request):
    return render(request, 'my_template.html')


def shop(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, "store/shop.html", context)





@login_required
def settingsview(request):
    # Assuming the user is logged in, you can access the UserProfile through request.user
    user= request.user
    
    
    return render(request, 'store/auth/settings.html', {'user_profile': user})



def categoryview(request,slug):
    print(slug)
    template="store/products/category.html"
    
    category=Category.objects.get(slug=slug)

   
    context={
        "category":category
       
    }
    return render(request,template,context)




def productview(request, pslug, vslug):
    template="store/products/product_view.html"
    # size = request.GET.get('size', '500ml')
    # request.GET = request.GET.copy()
    # request.GET['size'] = size

    # # try:
    # #     size = request.GET['size']
    # # except:
    # #     size='500ml'    
    # print(size)
    
    product = Product.objects.get(slug=pslug)
    variant = Variant.objects.get(product=product,slug=vslug)
    
    
    # sizevariants = Variant.objects.filter(product=product, size=size)
    # print(sizevariants)
    context={
        'variant' : variant
        
        # 'sizevariants' : sizevariants
    }
    return render(request,template,context)



@login_required 
def cart(request):
    
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0
    for item in cart_items:
        
        cart_total=cart_total+item.total_price
     
     
    promocode = PeromoCode.objects.filter(purchase_price__lte=cart_total)
    
    return render(request, 'store/products/cart.html', {'cart_items':cart_items, 'cart_total':cart_total, 'promocode':promocode} )
      
     
def cart_count_increase(request, id):
    print(id)
    cart_item = Cart.objects.get(id=id)
    cart_item.variant_qty += 1
    cart_item.save()
    return redirect('cart_page')     
     
     
def cart_count_decrease(request, id):
    print(id)
    cart_item = Cart.objects.get(id=id)
    if cart_item.variant_qty > 1:
       cart_item.variant_qty -= 1
       cart_item.save()
    
    
    return redirect('cart_page')     
          
     
@login_required          
def add_to_cart(request, slug ):
    
    print(slug)
    
    variant = Variant.objects.get(slug=slug)
    
    cart_iteam = Cart.objects.get_or_create(variant=variant, user=request.user)
    
    
    return redirect('cart_page')
    
@login_required
def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    
    return redirect('cart_page')
        
    
    
    
    
        
 