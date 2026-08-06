from rest_framework import serializers
from .models import StoreProfile

class StoreProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProfile
        fields = [
            "store_name",
            "description",
            "logo",
            "banner",
            "phone",
            "email",
            "address",
            "city",
            "country",
            "facebook",
            "instagram",
            "tiktok",
            "youtube",
            "created_at",
            "updated_at",
            ]