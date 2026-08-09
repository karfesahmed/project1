from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )
    updated_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )
    order_status = serializers.CharField(read_only=True)
    delivery_status = serializers.CharField(read_only=True)
    product_str = serializers.CharField(read_only=True)
    wilaya_code = serializers.CharField(read_only=True)
    wilaya_name = serializers.CharField(read_only=True)
    product_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    size_str = serializers.CharField(read_only=True)
    size_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    color_str = serializers.CharField(read_only=True)
    color_image = serializers.ImageField(read_only=True)
    delivery_cost = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'