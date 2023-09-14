from .models import *

from .serializers import *

from utility.global_functions import create_slug,runSerializer
from utility.variables import expecteddeliveryDays
from utility.pagination import StandardResultsSetPagination
from shoppingo.settings import logger
import traceback

from rest_framework.response import Response
from rest_framework import status,viewsets,permissions
from datetime import datetime,timedelta
from django.db import transaction


# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Order.objects.all()

 
    def retrieve(self, request, *args, **kwargs):
        try :
            orderId = kwargs['pk']
            # getting order with given order id, with order items with sql join
            order = Order.objects.filter(order_id = orderId).prefetch_related('orderitem_set')
            if not order.exists():
                raise Exception('order not found with given id!')
            
            order = order[0]
            
            serializer = self.serializer_class(order,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try :
            user = request.user
            # getting users order , with order items with sql join
            orders = Order.objects.filter(user = user).prefetch_related('orderitem_set')
            # paginating the orders
            page = self.paginate_queryset(orders)
            if page is not None:
                # serialize the page 
                serializer = self.serializer_class(page,many = True,context={'request':request})
               
                return self.get_paginated_response(serializer.data)
            
            serializer = self.serializer_class(orders,many = True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try :
            # add user to payload to create a order object
            user = request.user
            request.data['user'] = user.id

            today = datetime.now()
            request.data['order_date'] = today

            # create a order id
            orderId = create_slug(Order,lookUpField='order_id')
            # add order id in payload
            request.data['order_id'] = orderId

            # add expected devlivery date
            request.data['expected_delivery'] = today.date() + timedelta(days=expecteddeliveryDays)

            # create a order object 
            order,serializer = runSerializer(self.serializer_class , request.data)

            # creating order item objects, assuming item would be [{"product":productId,"quantity":1}]
            orderItems = request.data['items'] 
            for item in orderItems :
                # add order to ordr item data
                item['order'] = order.id
                runSerializer(OrderItemSerializer,data=item)
            
            return Response(serializer.data , status=status.HTTP_200_OK)
            
        except Exception as e :
            logger.warning(traceback.format_exc())
            transaction.set_rollback(True)  # Manually trigger a rollback so db will return to it's previous state
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
