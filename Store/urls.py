from django.urls import path
from . import views


urlpatterns = [
     
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("shop/<slug:slug>/", views.shopview, name="shopview"),
    path('shop/<str:slug>/', views.Productview, name="productview")
]
