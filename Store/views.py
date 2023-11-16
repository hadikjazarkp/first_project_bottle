from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404





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





def settingsview(request):
    return render(request,'store/auth/settings.html')





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
  


    
def add_to_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        quantity = request.POST.get('quantity', 1)

        try:
            variant = Variant.objects.get(pk=variant_id)
        except Variant.DoesNotExist:
            messages.error(request, 'Variant not found.')
            return redirect('home')  # Redirect to the home page or another appropriate URL

        # TODO: Implement your logic to add the item to the cart
        # You can use Django's session to store cart information
        # Example: 
        # cart = request.session.get('cart', [])
        # cart.append({'variant_id': variant.id, 'quantity': quantity})
        # request.session['cart'] = cart

        messages.success(request, 'Item added to the cart successfully.')
        return render(request,'store/products/cart.html')  # Redirect to the home page or another appropriate URL

    # Handle cases where the request method is not POST
    return redirect('home')  # Redirect to the home page or another appropriate URL
        
        
 