from django.urls import path 
from . import views

urlpatterns = [
    path('categories/',views.CategoryList.as_view(),name='category-list'),
    path('category/<int:pk>/',views.CategoryDetail.as_view(),name='category-detail'),
    path('products/',views.ProductList.as_view(),name='product-list'),
]