from rest_framework import serializers
from .models import *
from utility.mixins import FieldMixin
from home.serializers import ProductSerializer


class OrderItemSerializer(FieldMixin,serializers.ModelSerializer):
    # here we are putting a condition that we want ProductSerializer() for product field only when request is a GET method
    def to_representation(self, instance):
        # Get the request from the serializer's context
        request = self.context.get('request')

        # Check if the request method is GET
        if request and request.method == 'GET':
            # Serialize the product field using ProductSerializer
            self.fields['product'] = ProductSerializer()

        # Call the parent to_representation method
        return super(OrderItemSerializer, self).to_representation(instance)

    class Meta :
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField(read_only=True)

    class Meta :
        model = Order
        fields = '__all__'
    
    # serialize the items of order as well
    def get_order_items(self,obj):
        # get request to pass the in serializer 
        request = self.context.get('request')
        # getting order items of order along with product details
        orderItems = obj.orderitem_set.all().select_related('product')
        # serialize the order items and passing 'product' and 'qunatity' fields to serialize
        serializer  = OrderItemSerializer(orderItems,many=True,context = {'fields':['product','quantity'],'request':request})
        return serializer.data