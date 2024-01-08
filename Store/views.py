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
    sub_category = Sub_Category.objects.all()
    sort_by = request.GET.get('sort')
    
    category_by = request.GET.get('category')
    search_key = request.GET.get('search')
        
    
    
    
    
    
    
    # variant_items = [item.variants.first for item in Product.objects.all()]

    # if sort_by == 'new':
    #     # variant_items = sorted(variant_items, key=lambda x: x.created_at, reverse=True)
    #     pass
    # elif sort_by == 'low_to_high':
    #     variant_items = sorted(variant_items, key=lambda x: x.selling_price)
    # elif sort_by == 'high_to_low':
    #     variant_items = sorted(variant_items, key=lambda x: x.selling_price, reverse=True)
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
    else:
        cart_item.delete()
        
        
    
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
        
    
    
# @login_required    
# def checkout(request):
    
    
#     # process payment 
#     order_id ='123'
#     host = request.get_host()
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': '123',
#         'item_name': 'item_name',
#         'invoice': 'INV-123',
#         'currency_code': 'ISC',
#         'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
#         'return_url':'htpp://{}{}'.format(host,reverse('payment_done')),
#         'cancel_return':'htpp://{}{}'.format(host,reverse('payment_cancelled')),
        
        
#     } 
#     form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
#     total_amt=0
#     if 'cartdata' in request.session:
#         for p_id,item in request.session['cartdata'].items():
#             total_amt +=int(item['qty'])*float(item['price'])
#         return render(request, 'store/products/checkout_html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdat']), 'total_amt':total_amt, 'form':form})       
    
    
    
    
#     cart_items = Cart.objects.filter(user=request.user)
    
    
#     cart_total = 0
#     user_address = Address.objects.filter(user=request.user)
    
#     final_price = 0
    
    
#     for item in cart_items:
        
#         cart_total=cart_total+item.total_price
     
     
#     promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
#     discount_price = 0
#     if request.session.get('discount'):
#         discount_price = request.session.get('discount')
#         del request.session['discount']   
#     final_price = cart_total - discount_price
    
    
    
#     client =razorpay.Client( auth = (settings.KEY, settings.SECRET))
#     payment = client.order.create({'amount': (final_price) * 100, 'currency': 'INR', 'payment_capture': 1 }) 
#     item.rezor_pay_order_id = payment['id']
#     item.save()
   
    
    
#     return render(request, 'store/products/checkout.html', {'cart_items':cart_items, 'cart_total':cart_total, 'promocodes':promocodes, 'user_address':user_address, 'final_price':final_price, 'discount_price':discount_price, 'payment':payment})    




# @login_required
# def checkout(request):
    
    
#     total_amt = 0

#     totalAmt = 0
    
     
     
#     if 'cartdata' in request.session:
#         for p_id, item in request.session['cartdata'].items():
#             totalAmt += int(item['qty']) * float(item['price'])
#             host = request.get_host()
#         #order
#         order=CartOrder.objects.create(
#             user=request.user,
#             total_amt=totalAmt
#         )
#         #end
#         for p_id, item in request.session['cartdata'].items():
#             total_amt += int(item['qty']) * float(item['price'])
#             items=CartOrderItems(
#                 order=order,
#                 invoice_no='INV-'+str(order.id),
#                 item=item['title'],
#                 image=item['image'],
#                 qty=item['qty'],
#                 price=item['price'],
#                 total=float(item['qty'])*float(item['price'])               
#                 )
#         host = request.get_host()
#         paypal_dict = {
#                 'business': settings.PAYPAL_RECEIVER_EMAIL,
#                 'amount': '123',
#                 'item_name': 'OrderNo-'+str(order.id),
#                 'invoice': 'INV-'+str(order.id),
#                 'currency_code': 'ISC',
#                 'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
#                 'return_url':'htpp://{}{}'.format(host,reverse('payment_done')),
#                 'cancel_return':'htpp://{}{}'.format(host,reverse('payment_cancelled')),
        
#             }

#         form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
#         return render(request, 'store/products/checkout_html', {'cart_data': request.session['cartdata'],
#                                                                 'totalitems': len(request.session['cartdat']),
#                                                                 'total_amt': total_amt, 'form': form})

#     cart_items = Cart.objects.filter(user=request.user)
    
#     cart_total = sum(item.total_price for item in cart_items)
#     user_address = Address.objects.filter(user=request.user)
    
#     promocodes = PromoCode.objects.filter(purchase_price__lte=cart_total)
#     discount_price = request.session.get('discount', 0)
#     final_price = cart_total - discount_price

#     try:
#         client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#         payment = client.order.create({'amount': int(final_price * 100), 'currency': 'INR', 'payment_capture': 1})
        
#         # Assuming you have a loop here to handle multiple cart items
#         for item in cart_items:
#             item.razor_pay_order_id = payment['id']
#             item.save()
#     except ConnectionError as e:
#         # Handle the connection error, e.g., log the error or inform the user
#         return render(request, 'store/products/checkout.html', {'error_message': 'Failed to connect to Razorpay. Please try again later.'})

#     return render(request, 'store/products/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total,
#                                                             'promocodes': promocodes, 'user_address': user_address,
#                                                             'final_price': final_price, 'discount_price': discount_price,
#                                                             'payment': payment})
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


@csrf_exempt
def payment_done(request):
    returnData=request.POST
    return render(request, 'store/products/payment-success.html',{'data':returnData})   

@csrf_exempt
def payment_canceled(request):
    return render(request, 'store/products/payment-fail.html')



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




def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def placeorder(request):
    if request.method == 'POST':
        # neworder = Order()
        # neworder.user = request.user
        # neworder.first_name = request.POST.get('first_name')
        # neworder.address_type = request.POST.get('address_type')
        # neworder.address = request.POST.get('address')
        # neworder.city = request.POST.get('city')
        # neworder.state = request.POST.get('state')
        # neworder.phone_number = request.POST.get('phone_number')
        # neworder.pincode = request.POST.get('pincode')
       
        
        # neworder.payment_mode = request.POST.get('payment_mode')
        # neworder.total_price = request.POST.get('final_price')
        # trackno = 'usbot'+str(random.randint(1111111,9999999))
        print("cgbgfn")
        
        
        user = request.user
        address = request.POST.get('selectedAddressData')
        payment_mode = request.POST.get('payment_mode')
        total_price = request.POST.get('final_price')
        trackno = 'usbot'+str(random.randint(1111111,9999999))
        print("user",user,"address",address,"payment_mode",payment_mode,"total_price",total_price,"trackno",trackno)
        # while Order.objects.filter(tracking_no=trackno) is None:
        #     trackno = 'usbot'+str(random.randint(1111111,9999999))
            
        # neworder.tracking_no = trackno
        # neworder.save()
        
        
        # neworderitems = Cart.objects.filter(user=request.user)
        # for item in neworderitems:
        #     OrderItem.objects.create(
        #         order=neworder,
        #         variant=item.variant,
        #         quantity=item.variant_qty,
        #         price=item.variant.selling_price
                
        #     )    

        #     # To decrease the product quantity from available stock
        #     orderproduct = Variant.objects.filter(id=item.id).first()
        #     orderproduct.quantity = orderproduct.quantity - item.variant_qty
        #     orderproduct.save()
            
        # # To clear user Cart
        # Cart.objects.filter(user=request.user).delete()  
        
        # messages.success(request, "Youe order has been placed successfuly")  

    return redirect('home')
    