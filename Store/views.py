from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404



def home(request):
    print(request.user.username)
    main_images = Main_Images.objects.first()
    return render(request,"store/index.html", {'main_images': main_images})



def my_view(request):
      # Get the first instance of Main_Images
    return render(request, 'my_template.html')


def shop(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, "store/shop.html", context)





def categoryview(request,slug):
    print(slug)
    template="store/products/category.html"
    
    category=Category.objects.get(slug=slug)

    # for sub_category in sub_categoris:
    #     sub_category
    #     products = Product.objects.filter(sub_category=sub_category)
    #     for product in products:
    #         print(product)
    # products=Product.objects.filter(category=category)
    
    context={
        "category":category
        # "products":products,
    }
    return render(request,template,context)




def productview(request, slug):
    template="store/products/product_view.html"
    sub_category = Sub_Category.objects.get(slug=slug)
    context={
        'sub_product':sub_category
    }
    return render(request,template,context)
    print(slug)
#     product = get_object_or_404(Product, slug=slug)
#     context = {'product': product}
#     return render(request, "store/products/view.html", context)   

  

        
        
 