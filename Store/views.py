from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages


def home(request):
    return render(request,"store/index.html")


def shop(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, "store/shop.html", context)


def shopview(request,slug):
    
    template="store/products/index.html"
    
    categories=Category.objects.get(slug=slug)
    products=Product.objects.filter(category=categories)
    context={
        "products":products,
    }
    return render(request,template,context)
    
    # if(Category.objects.filter(slug=slug, status=0)):
    #     products = Product.objects.filter(category__slug=slug)
    #     category_name = Category.objects.filter(slug=slug).first()
    #     context = {'products': products, 'category_name':category_name}
    #     return render(request, "store/products/index.html", context)
    # else:
    #     messages.warning(request, "No search category found")
    #     return redirect('shop')