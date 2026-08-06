from django.urls import path
from .views import StoreProfileDetail

urlpatterns = [
    path("store-profile/",StoreProfileDetail.as_view(),name="store_profile")
]