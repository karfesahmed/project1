from django.urls import path
from .views import AddProductView, DashboardView, HomeView

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
    path("addproduct/",AddProductView.as_view(),name="add_product")
]