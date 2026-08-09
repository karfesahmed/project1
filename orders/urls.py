from django.urls import path
from . import views

urlpatterns = [
    path("create-order/",views.OrderCreate.as_view()),
    # path("orders/",views.OrderList.as_view())
]