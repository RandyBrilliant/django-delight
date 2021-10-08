from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name="home"),

    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', views.sign_out, name="logout"),

    path('ingredient/', views.ListIngredient.as_view(), name="ingredient"),
    path('ingredient/add/', views.CreateIngredient.as_view(), name="add-ingredient"),
    path('ingredient/<slug:slug>/', views.UpdateIngredient.as_view(), name="ingredient-detail"),
    path('ingredient/<slug:slug>/delete/', views.DeleteIngredient.as_view(), name="delete-ingredient"),
    
    path('menu-item/', views.ListMenu.as_view(), name="menu-item"),
    path('menu-item/add/', views.CreateMenu.as_view(), name="add-menu"),
    path('menu-item/<slug:slug>/', views.UpdateMenu.as_view(), name="menu-detail"),
    path('menu-item/<slug:slug>/delete/', views.DeleteMenu.as_view(), name="delete-menu"),

    path('purchase/', views.ListPurchase.as_view(), name="purchase"),
    path('purchase/record/', views.CreatePurchase.as_view(), name="record-purchase"),
]
