from django.urls import path
from . import views


urlpatterns = [
     
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("category/<slug:slug>/", views.categoryview, name="categoryview"),
    path('product/<str:slug>/', views.Productview, name="productview")
]
