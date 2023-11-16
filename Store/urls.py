from django.urls import path
from . import views

from Store.controller import authview 

urlpatterns = [
     
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.categoryview, name="categoryview"),
    path("product/<slug:pslug>/<slug:vslug>/", views.productview, name="productview"),
    
    
    path("settings/", views.settingsview, name='settingsview'),
    
   
    path('register/', authview.Register.as_view(), name="register"),
    path('verify/<str:key>/',authview.VerifyOtpView.as_view(),name='otp'),
    path('resend_otp/<str:key>/', authview.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', authview.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',authview.UserResetPassword.as_view(),name='reset'),
    path('login/',authview.SignIn.as_view(), name="loginpage"),
    path('logout/', authview.Logoutpage.as_view(), name="logout"),
]
