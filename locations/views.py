from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Wilaya,Commune
from .serializers import DeliverySettingsSerializer, WilayaSerializer,CommuneSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
# Create your views here.


# @api_view(["GET","POST"])
# def wilaya_list(request):
#     if request.method == 'GET':
#         wilayas = Wilaya.objects.all()
#         serializer = WilayaSerializer(wilayas,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = WilayaSerializer(data = request.data,many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WilayaList(generics.ListCreateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    
# @api_view(["GET","POST"])
# def commune_list(request):
#     if request.method == 'GET':
#         communes = Commune.objects.all()
#         serializer = CommuneSerializer(communes,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = CommuneSerializer(data = request.data,many=True)
#         if serializer.is_valid():
#             print(serializer.data)
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommuneList(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    def get_serializer(self, *args, **kwargs):
        kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    
# @api_view(["PATCH"])
# def delivery_settings(request,wilaya_id):
#     try:
#         wilaya = Wilaya.objects.get(code=wilaya_id)
#     except Wilaya.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "PATCH":
#         serializer = DeliverySettingsSerializer(wilaya,data = request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliverySettings(generics.UpdateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = DeliverySettingsSerializer
    lookup_url_kwarg = 'wilaya_code'
    lookup_field = 'code'

# @api_view(["GET"])
# def wilaya_communes(request,wilaya_id):
#     try:
#         wilaya = Wilaya.objects.get(code=wilaya_id)
#     except Wilaya.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         communes = Commune.objects.filter(wilaya = wilaya)
#         serializer = CommuneSerializer(communes,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
class WilayaCommunes(generics.ListAPIView):
    serializer_class = CommuneSerializer
    def get_queryset(self):
        return Commune.objects.filter(
            wilaya__code = self.kwargs["wilaya_code"]
        )