import datetime

from django.shortcuts import render
from django.views.generic import TemplateView

from products import serializers

class HomeView(TemplateView):
    template_name = "client/home.html"

class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

class AddProductView(TemplateView):
    template_name = "dashboard/add_product.html"


