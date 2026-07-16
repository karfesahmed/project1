from django.urls import path
from . import views

urlpatterns = [
    path("wilayas",views.WilayaList.as_view()),
    path("wilaya/<str:wilaya_code>",views.DeliverySettings.as_view()),
    path("communes",views.CommuneList.as_view()),
    path("wilaya/<str:wilaya_code>/communes",views.WilayaCommunes.as_view()),
]