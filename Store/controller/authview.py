from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from Store.forms import CustomUserForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form =CustomUserForm()
    if request.method == 'POST':
        form =CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Register Seccessfully! Login to Continue")
            return redirect('login')
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
    
           
    
    
    