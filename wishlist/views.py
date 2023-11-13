from django.shortcuts import render
from django.views import View
from .models import *
from Store.models import *
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.


class WishlistView(View):
    def get(self, request):
    
        # Try to retreve the user's wishlist, or created one if it doesn't exist
        wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
            
         # Check if wishlist is None or if it's created and product field is None
        if wishlist is not None and wishlist.product is not None:
            wishlist_items = wishlist.product.all()
        else:
            wishlist_items = [] # Initialize an emty list if wishlist or product is None 
        print(wishlist_items)
        return render(request, 'store/products/wishlist.html', {'wishlist_items': wishlist_items})
        


class AddToWishlistView(View):
    def post(self, request, slug):
    
           #this view is only accessible to authenticated users.
        product = get_object_or_404(Product, slug=slug)
        wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
        wishlist.product.add(product) # Assuming you have a 'products' filed for the wishlist
        return redirect('wishlist_view')
       
        

class RemoveFromWishlistView(View):
    def post(self, request, slug):
        
        product = get_object_or_404(Product, slug=slug)
        wishlist = WishlistModel.objects.get(user=request.user)
        wishlist.product.remove(product)
        # Remove the product from the wishlist
        return redirect('wishlist_view') 
        