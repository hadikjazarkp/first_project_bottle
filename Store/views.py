from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404





def home(request):
    print(request.user.username)
    main_images = Main_Images.objects.first()
    return render(request,"store/index.html", {'main_images': main_images})



def my_view(request):
    return render(request, 'my_template.html')


def shop(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, "store/shop.html", context)





def categoryview(request,slug):
    print(slug)
    template="store/products/category.html"
    
    category=Category.objects.get(slug=slug)

   
    context={
        "category":category
       
    }
    return render(request,template,context)




def productview(request, slug):
    template="store/products/product_view.html"
    product = Product.objects.get(slug=slug)
    context={
        'product':product
    }
    return render(request,template,context)
  

  

        
        
 