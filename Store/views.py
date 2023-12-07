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
    user_address = Address.objects.filter(user=request.user)
    
    return render(request, 'store/auth/settings.html', {'user_profile': user, 'user_address':user_address})



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




@login_required(login_url='loginpage')  # Specify the login URL
def cart(request):

        
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0
    for item in cart_items:
        
        cart_total=cart_total+item.total_price
     
     
    
    
    return render(request, 'store/products/cart.html', {'cart_items':cart_items, 'cart_total':cart_total,} )
      
     
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
        
    
    
    
def checkout(request):
    
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0
    user_address = Address.objects.filter(user=request.user)
    
    final_price = 0
    
    
    for item in cart_items:
        
        cart_total=cart_total+item.total_price
     
     
    promocodes = PeromoCode.objects.filter(purchase_price__lte=cart_total)
    discount_price = 0
    if request.session.get('discount'):
        discount_price = request.session.get('discount')
        del request.session['discount']   
    final_price = cart_total - discount_price
    
    
    return render(request, 'store/products/checkout.html', {'cart_items':cart_items, 'cart_total':cart_total, 'promocodes':promocodes, 'user_address':user_address, 'final_price':final_price, 'discount_price':discount_price})    

   
from django.shortcuts import render, redirect

def add_address(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')  # Updated to match the HTML form
        pincode = request.POST.get('pincode') 
        address_type = request.POST.get('address_type')

        # Print the values for testing
        Address.objects.create(first_name=first_name,last_name=last_name,address=address,city=city,state=state,phone_number=phone_number,pincode=pincode,address_type=address_type, user=request.user)
        print(first_name, last_name, address, city, state, phone_number,pincode, address_type)

        # Perform any additional processing or save to the database as needed

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the referring page or home if not available


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        # Process the form data if needed, you can access it using request.POST
        # Update the address fields accordingly
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.address_type = request.POST.get('address_type')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.phone_number = request.POST.get('phone_number')
        address.pincode = request.POST.get('pincode')
        
        # Save the updated address
        address.save()
        
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    # if request.method == 'POST':
    address.delete()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))


        
     
# def checkout_increase(request, id):
#     print(id)
#     cart_item = Cart.objects.get(id=id)
#     cart_item.variant_qty += 1
#     cart_item.save()
#     return redirect('checkout')     
     
     
# def checkout_count_decrease(request, id):
#     print(id)
#     cart_item = Cart.objects.get(id=id)
#     if cart_item.variant_qty > 1:
#        cart_item.variant_qty -= 1
#        cart_item.save()
    
    
#     return redirect('checkout')     
          
  
  
  
def promocode_view(request):
    
    # cart_items = Cart.objects.filter(user=request.user)
    promocode_value = request.POST.get('promocodevalue')
    cart_total_price = request.POST.get('cart_total')
    
    
    if promocode_value is not None:
        discount = float(promocode_value)
        # cart_total_price = float(cart_total_price)

        # discount = cart_total_price - promocode_value
    request.session['discount']= discount

        
    # print(promocode_value)
    # print(discount)
    
    
    
    
    

    
    return redirect(request.META.get('HTTP_REFERER'))
