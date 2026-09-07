from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class ProductPagination(PageNumberPagination):
    page_size = 10


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    
class ProductList(generics.ListAPIView):
    
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        'category__slug':["exact","iexact"],
        
    }
    search_fields = [
        "name"
    ]
    ordering_fields = [
        'price',
        'created_at'
    ]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        return queryset.select_related(
            "category"
            ).prefetch_related(
                "images",
                "colors",
                "sizes"
                )
   

class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]