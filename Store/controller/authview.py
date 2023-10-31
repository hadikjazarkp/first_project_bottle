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
    
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Send success message and OTP email
            messages.success(request, "Registered Successfully! Login to Continue")
            otp = str(random.randint(100000, 999999))
            send_otp_email(user.email, user.username, otp)

            # Generate cache key and store registration data
            key = hashlib.sha256(user.email.encode()).hexdigest()
            cache.set(
                key,
                {"email": user.email, "username": user.username, "password": form.cleaned_data['password1'], "otp": otp},
                timeout=600
            )

            # Redirect to OTP verification
            return redirect("otp", key=key) 

    context = {'form': form}
    return render(request, "store/auth/register.html", context )

class VerifyOtpView(View):
    def get(self, request, key):
        # Render the OTP verification form
        return render(request, "store/auth/otp.html", {"key": key})

    def post(self, request, key):
        receivedotp = request.POST.get("otp")

        signup_data = cache.get(key)
        print(signup_data)
        if not signup_data:
            messages.warning(request, "OTP expired or invalid")
            return redirect("otp", key=key)
        otp = signup_data.get("otp")
        username = signup_data.get("username")
        email = signup_data.get("email")
        password = signup_data.get("password")
        print(receivedotp, otp)
        if receivedotp != otp:
            messages.warning(request, "OTP mismatch")
            return redirect("otp", key=key)

        user = UserProfile.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        cache.delete(key)
        return redirect("login")



class ResendOTP(View):
    def get(self, request, key):
        signup_data = cache.get(key)
        if signup_data:
            email = signup_data.get("email")
            username = signup_data.get("username")
            otp = str(random.randint(100000, 999999))
            print(otp)
            send_otp_email(email, username, otp)
            signup_data["otp"] = otp
            existing_timeout = signup_data.get("timeout", None)
            cache.set(key, signup_data, timeout=existing_timeout)
            return redirect("otp", key=key)
        return redirect("signup")


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
    
           
    
    
    