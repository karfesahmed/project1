from .models import Wilaya,Commune
from .serializers import DeliverySettingsSerializer, WilayaSerializer,CommuneSerializer
from rest_framework import generics


class WilayaList(generics.ListCreateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer

class CommuneList(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    def get_serializer(self, *args, **kwargs):
        kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

class DeliverySettings(generics.UpdateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = DeliverySettingsSerializer
    lookup_url_kwarg = 'wilaya_code'
    lookup_field = 'code'

class WilayaCommunes(generics.ListAPIView):
    serializer_class = CommuneSerializer
    def get_queryset(self):
        return Commune.objects.filter(
            wilaya__code = self.kwargs["wilaya_code"]
        )