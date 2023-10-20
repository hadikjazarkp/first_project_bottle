from django.urls import path
from . import views

from Store.controller import authview 

urlpatterns = [
     
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.category_view, name="category_view"),
    path('sub_category/<str:slug>/', views.sub_category, name="sub_categoryw"),
   
   
    path('register/', authview.register, name="register"),
    path('login/',authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
]
