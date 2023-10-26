from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .email import *
from Store.models import UserProfile
from Store.forms import CustomUserForm

from django.core.cache import cache
import hashlib
import random
from django.views import View
from Store.forms import CustomUserForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form =CustomUserForm()
    if request.method == 'POST':
        form =CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            otp = str(random.rendint(100000, 999999))
            send_otyp_email(form.email, form.username, otp)
            key = hashlib.sha256(form.email.encode()).hexdigest()
            cache.set(
                key,
                {"email": form.email, "username": form.username, "password":form.password1, "otp": otp},
                timeout=600,
            )
            messages.success(request,"Register Seccessfully! Login to Continue")
            return redirect('')
        
    context = {'form':form}
    return render(request, "store/auth/register.html", context )

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "YOU are already logged in")
        return redirect('home')
    else: 
        if request.method == 'POST':
            email = request.POST.get('email')
            passwd = request.POST.get('password')
        
            user = authenticate(request, email=email, password=passwd)
        
            if user is not None:
               login(request, user)
               messages.success(request, "Logged in Successfully")
               return redirect("home")
            else:
               messages.error(request, "Invalid Username or Password")
        return render(request, "store/auth/login.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully ")
        return redirect("home")
    
           
    
    
    