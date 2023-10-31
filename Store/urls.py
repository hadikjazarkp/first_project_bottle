from django.urls import path
from . import views

from Store.controller import authview 

urlpatterns = [
     
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.categoryview, name="categoryview"),
    path("product/<slug:slug>/", views.productview, name="productview"),

    
   
    path('register/', authview.register, name="register"),
    path('verify/<str:key>/',authview.VerifyOtpView.as_view(),name='otp'),
    path('resend_otp/<str:key>/', authview.ResendOTP.as_view(), name='resend_otp'),
    path('login/',authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
]
