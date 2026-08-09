from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .serializers import OrderSerializer
from .models import Order
from rest_framework.exceptions import ValidationError


# class OrderList(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class OrderCreate(generics.CreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]