from django.shortcuts import get_object_or_404
from .models import StoreProfile
from accounts.models import User
from .serializers import StoreProfileSerializer
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
class StoreProfileDetail(generics.RetrieveUpdateAPIView):
    def get_object(self):
        user = get_object_or_404(User,is_superuser=True)
        store_profile , created = StoreProfile.objects.get_or_create(user = user)
        return store_profile

    serializer_class = StoreProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]