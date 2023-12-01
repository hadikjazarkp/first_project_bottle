from django.urls import path
from . import views

from Store.controller import authview 

urlpatterns = [
     
  
         
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.categoryview, name="categoryview"),
    path("product/<slug:pslug>/<slug:vslug>/", views.productview, name="productview"),
    path("settings/", views.settingsview, name='settingsview'),
    
    path("cart/", views.cart, name='cart_page'),
    path('cart_count_increment/<uuid:id>/', views.cart_count_increase, name="cart_count_increment"),
    path('cart_count_decrement/<uuid:id>/', views.cart_count_decrease, name="cart_count_decrement"),
    path("add_to_cart/<slug:slug>/", views.add_to_cart, name='add_to_cart'),
    path("remove_from_cart/<uuid:id>/",views.remove_from_cart, name='remove_from_cart'),
     
    path('checkout/', views.checkout, name='checkout'),
    path('add_address/', views.add_address, name='add_address'),
    # path('checkout_count_increment/<uuid:id>/', views.checkout_increase, name="checkout_increase"),
    # path('checkout_count_decrement/<uuid:id>/', views.checkout_count_decrease, name="checkout_count_decrease"),
    
   
    path('register/', authview.Register.as_view(), name="register"),
    path('verify/<str:key>/',authview.VerifyOtpView.as_view(),name='otp'),
    path('resend_otp/<str:key>/', authview.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', authview.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',authview.UserResetPassword.as_view(),name='reset'),
    path('login/',authview.SignIn.as_view(), name="loginpage"),
    path('logout/', authview.Logoutpage.as_view(), name="logout"),
]


