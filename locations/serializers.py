from email.policy import default

from rest_framework import serializers
from .models import Wilaya, Commune

class WilayaListSerializer(serializers.ListSerializer):
    def create(self,validated_data):
        wilayas = [Wilaya(**wilaya) for wilaya in validated_data]
        Wilaya.objects.all().delete()
        return Wilaya.objects.bulk_create(wilayas)
    
class CommuneListSerializer(serializers.ListSerializer):
    
    def create(self,validated_data):
        print(validated_data)
        communes = [Commune(**commune) for commune in validated_data]
        Commune.objects.all().delete()
        return Commune.objects.bulk_create(communes)

class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = '__all__'
        list_serializer_class = WilayaListSerializer

class CommuneSerializer(serializers.ModelSerializer):
    wilaya_id = serializers.SlugRelatedField(
        source="wilaya",
        slug_field="code",
        queryset=Wilaya.objects.all(),
        write_only=True
    )

    wilaya = serializers.CharField(source="wilaya.code", read_only=True)

    class Meta:
        model = Commune
        fields = [
            "id",
            "wilaya",
            "wilaya_id",
            "name",
            "ar_name",
        ]
        list_serializer_class = CommuneListSerializer
class DeliverySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['delivery_price','is_available']