from django.shortcuts import get_object_or_404
from .models import StoreProfile
from accounts.models import User
from .serializers import StoreProfileSerializer
from rest_framework import generics,permissions
from .permissions import IsOwnerOrReadOnly

class StoreProfileDetail(generics.RetrieveUpdateAPIView):
    def get_object(self):
        
        user = get_object_or_404(User,is_superuser=True)
        obj = get_object_or_404(StoreProfile,user = user)
        self.check_object_permissions(self.request, obj)
        return obj

    serializer_class = StoreProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]