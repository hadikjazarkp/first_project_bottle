from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from paypal.standard.forms import PayPalEncryptedPaymentsForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from django.http import HttpResponse
import random
from django.http import JsonResponse
from django.utils.decorators import method_decorator


from django.shortcuts import render
from .models import Main_Images, Category, Product

def home(request):
    main_images = Main_Images.objects.first()
    category = Category.objects.all()
    all_products = Product.objects.all()

    # Create a new variable containing the first 6 products, sorted by creation date
    six_products = all_products.order_by('created_at')[:6]

    return render(request, "store/index.html", {'main_images': main_images, 'category': category, 'product': all_products, 'six_products': six_products})



def my_view(request):
    return render(request, 'my_template.html')


def shop(request):
    category = Category.objects.all()
    sub_category = Sub_Category.objects.all()
    sort_by = request.GET.get('sort')
    
    category_by = request.GET.get('category')
    search_key = request.GET.get('search')
        
    
    
    
    
    
    
    products = Product.objects.all()

    if sort_by == 'new':
        # Sort the products by the created_at attribute of their variants
        products = products.order_by('-variants__created_at')
    elif sort_by == 'low_to_high':
        # Sort the products by the selling_price attribute of their variants
        products = products.annotate(min_price=models.Max('variants__selling_price')).order_by('min_price')
    elif sort_by == 'high_to_low':
        # Sort the products by the selling_price attribute of their variants in reverse order
        products = products.annotate(max_price=models.Max('variants__selling_price')).order_by('-max_price')
    if category_by:
        products = products.filter(sub_category__category__slug = category_by)  
    if search_key:
        products = Product.objects.filter( Q(variants__color__istartswith=search_key) | Q(name__istartswith=search_key) | Q(sub_category__category__name__istartswith=search_key) | Q(sub_category__name__istartswith=search_key) )      
   
    context = {
        'category':category,
        'sub_category' : sub_category,
        'products' :products,
        }
    return render(request, "store/shop.html", context)





@login_required
def settingsview(request):
    # Assuming the user is logged in, you can access the UserProfile through request.user
    user= request.user
    user_address = Address.objects.filter(user=request.user)
    first_address = Address.objects.filter(user=request.user).first()
    return render(request, 'store/auth/settings.html', {'user_profile': user, 'user_address':user_address,'first_address':first_address})



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
 
    
    product = Product.objects.get(slug=pslug)
    variant = Variant.objects.get(product=product,slug=vslug)
    
    
    context={
        'variant' : variant
        
       
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
    
    cart_item = Cart.objects.get(id=id)
    cart_item.variant_qty += 1
    cart_item.save()
    return redirect('cart_page')     
     
     
def cart_count_decrease(request, id):
    
    cart_item = Cart.objects.get(id=id)
    if cart_item.variant_qty > 1:
       cart_item.variant_qty -= 1
       cart_item.save()
    else:
        cart_item.delete()
        
        
    
    return redirect('cart_page')     
          
     
@login_required(login_url='loginpage')  # Specify the login URL
def add_to_cart(request, slug ):
    print(slug)
    variant = Variant.objects.get(slug=slug)
    cart_iteam = Cart.objects.get_or_create(variant=variant, user=request.user)
    return redirect('cart_page')

def add_to_cart_button(request, slug):
    try:
        variant = Variant.objects.get(slug=slug)
        cart_item, created = Cart.objects.get_or_create(variant=variant, user=request.user)
        if created:
            message = "Product added to cart successfully"
        else:
            message = "Product already in the cart"

        return JsonResponse({'success': True, 'message': message})
    except Variant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)


# def add_to_cart_button(request, slug ):
    
#     print(slug)
    
#     variant = Variant.objects.get(slug=slug)
    
#     cart_iteam = Cart.objects.get_or_create(variant=variant, user=request.user)
#     messages.success(request, "Your Product added has been placed successfully") 
    
#     return redirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
def remove_from_cart(request, slug):
    print(slug)
    try:
        item = get_object_or_404(Cart, slug=slug, user=request.user)
        print(item)
        item.delete()
        messages.success(request, "Your product has been removed from the cart successfully")
        return JsonResponse({'success': True, 'message': 'Item removed successfully'})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
  
                                                    
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0
    user_address = Address.objects.filter(user=request.user)
    
    final_price = 0
    
    
    for item in cart_items:
        
        cart_total=cart_total+item.total_price
     
     
    promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
    discount_price = 0
    if request.session.get('discount'):
        discount_price = request.session.get('discount')
        del request.session['discount']   
    final_price = cart_total - discount_price

    client =razorpay.Client( auth = (settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': (final_price) * 100, 'currency': 'INR', 'payment_capture': 1 }) 
    item.rezor_pay_order_id = payment['id']
    item.save()



    return render(request, 'store/products/checkout.html', {'cart_items':cart_items, 'cart_total':cart_total, 'promocodes':promocodes, 'user_address':user_address, 'final_price':final_price, 'discount_price':discount_price, 'payment':payment})   




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


        
# def promocode_view(request):
#     if request.method == 'POST':
#         promocode_value = request.POST.get('promocodevalue')
#         cart_total_price = request.POST.get('cart_total')
#         print(promocode_value,cart_total_price)
#         try:
#             discount = float(promocode_value)
#         except ValueError:
#             # Handle the case where promocode_value is not a valid float
#             discount = 0  # Set a default value or handle the error accordingly

#         request.session['discount'] = discount

    # return redirect(request.META.get('HTTP_REFERER'))

# <script>
#   function openPromoModal() {
#     document.getElementById('promoModal').classList.remove('hidden');
#   }

#   function closePromoModal() {
#     $('#promoModal').addClass('hidden');
# }

# const promocodeForm = $('#myform');

# promocodeForm.submit((e) => {
#     e.preventDefault();

#     const formData = promocodeForm.serialize();

#     $.ajax({
#         type: 'POST',
#         url: '/promocode_view/',
#         data: formData,
#         success: function(response) {
#             console.log(response);
#             alert('Promo code applied successfully');
#             location.reload();
#         },
#         error: function(error) {
#             if (error.status === 403) {
#                 alert('Please login to add items to the cart');
#                 window.location.href = '/loginpage/';
#             } else {
#                 console.error('Error applying promo code', error);
#             }
#         },
#         complete: function() {
#             closePromoModal();
#         }
#     });
# });

# // Close the modal
# closePromoModal();

  
  
  
  
#  <div id="promoModal" class="modal fixed hidden inset-0 flex items-center justify-center">
#     <form id="myform" method="post">
#         {% csrf_token %}
#         <input type="hidden" name="cart_total" value="{{ cart_total }}">
#         <div class="modal-content bg-white border rounded-lg shadow-md p-8 ">
#             <span onclick="closePromoModal()" class="close text-3xl font-semibold cursor-pointer">&times;</span>

#             <div class="mb-6">
#                 <label for="promoCode" class="block text-gray-700 text-sm font-bold mb-2">Select Promo Code:</label>
#                 <select name="promocodevalue" id="promoCode" class="w-full border rounded py-2 px-3 focus:outline-none focus:shadow-outline-blue focus:border-blue-300">
#                     {% for promocode in promocodes %}
#                         <option id="idd" value="{{ promocode.discount_price }}">{{ promocode.code }} - {{ promocode.discount_price }}</option>
#                     {% endfor %}
#                 </select>
#             </div>

#             <div class="text-center">
#                 <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
#                     Apply
#                 </button>
#             </div>
#         </div>
#     </form>
# </div>
  
  
def promocode_view(request):
    
    # cart_items = Cart.objects.filter(user=request.user)
    promocode_value = request.POST.get('promocodevalue')
    cart_total_price = request.POST.get('cart_total')
    
    
    if promocode_value is not None:
        discount = float(promocode_value)
        # cart_total_price = float(cart_total_price)

        # discount = cart_total_price - promocode_value
    request.session['discount']= discount

    return redirect(request.META.get('HTTP_REFERER'))




@login_required
def placeorder(request):
    if request.method == 'POST':
        # neworder = Order()
        # neworder.user = request.user
        
        address = request.POST.get('selectedAddressId').strip()
        address = Address.objects.get(id=address)
        
        
        payment_mode = request.POST.get('payment_mode')
        total_price = request.POST.get('final_total')
        coupon=request.POST.get('discount_price')
        print(coupon)
        # # Ensure that the tracking number is unique
        trackno = 'usbot' + str(random.randint(1111111, 9999999))
        while UserOrder.objects.filter(tracking_no=trackno).exists():
            trackno = 'usbot' + str(random.randint(1111111, 9999999))
        
        # neworder.tracking_no = trackno
        # neworder.save()
        neworder= UserOrder.objects.create(user=request.user,address=address,total_price=total_price,payment_mode=payment_mode,tracking_no=trackno)
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            UserOrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                quantity=item.variant_qty,
                price=item.variant.selling_price,
                total=total_price,
                coupon=coupon
                
            )    

            # To decrease the product quantity from available stock
            orderproduct = Variant.objects.get(id=item.variant.id)
            orderproduct.quantity = orderproduct.quantity - item.variant_qty
            orderproduct.save()
            
        # To clear user Cart
        Cart.objects.filter(user=request.user).delete()  
        
        messages.success(request, "Your order has been placed successfully")  

    return redirect('home')


def profile_view(request):
    return render(request, 'store/auth/profile.html',)
    

def profile_order(request):
    orders = UserOrder.objects.filter(user=request.user)
    context = { 'order':orders }
    return render(request, 'store/auth/order.html', context)    


def profile_address(request):
    user= request.user
    user_address = Address.objects.filter(user=request.user)
    first_address = Address.objects.filter(user=request.user).first()
    return render(request, 'store/auth/address.html', {'user_profile': user, 'user_address':user_address,'first_address':first_address})