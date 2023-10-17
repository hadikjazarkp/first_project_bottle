from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404



def home(request):
    return render(request,"store/index.html")






def shop(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, "store/shop.html", context)





def categoryview(request,slug):
    print(slug)
    template="store/products/index.html"
    
    category=Category.objects.get(slug=slug)
    products=Product.objects.filter(category=category)
    context={
        "category":category,
        "products":products,
    }
    return render(request,template,context)






def Productview(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, "store/products/view.html", context)   

  

        
        
        
        
        
        