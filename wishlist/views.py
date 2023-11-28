from django.shortcuts import render
from django.views import View
from .models import *
from Store.models import *
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class WishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))  # Redirect to the login page if not authenticated
    def get(self, request):
        wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
        if wishlist is not None and wishlist.product is not None:
            wishlist_items = wishlist.product.all()
        else:
            wishlist_items = []
        print(wishlist_items)
        return render(request, 'store/products/wishlist.html', {'wishlist_items': wishlist_items})

class AddToWishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        wishlist, created = WishlistModel.objects.get_or_create(user=request.user)
        wishlist.product.add(product)
        return redirect('wishlist_view')

class RemoveFromWishlistView(View):
    @method_decorator(login_required(login_url='loginpage'))
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        wishlist = WishlistModel.objects.get(user=request.user)
        wishlist.product.remove(product)
        return redirect('wishlist_view')