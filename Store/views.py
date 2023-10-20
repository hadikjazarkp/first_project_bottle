from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404



def home(request):
    print(request.user.username)
    return render(request,"store/index.html")






def shop(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, "store/shop.html", context)





# def categoryview(request,slug):
#     print(slug)
#     template="store/products/index.html"
    
#     category=Category.objects.get(slug=slug)
#     products=Product.objects.filter(category=category)
#     context={
#         "category":category,
#         "products":products,
#     }
#     return render(request,template,context)



def category_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "store/category.html", context)


def sub_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    subcategories = Sub_Category.objects.filter(category_id=category)
    
    context = {'category': category, 'subcategories': subcategories}
    return render(request, "store/sub_category.html", context)
    



# def Productview(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     context = {'product': product}
#     return render(request, "store/products/view.html", context)   

  

        
        
 