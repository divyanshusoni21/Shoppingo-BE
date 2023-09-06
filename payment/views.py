from .models import *

from .serializers import *

from shoppingo.settings import logger,RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
import traceback

from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
import razorpay

client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))


# Create your views here.
class PaymentInitializeViewSet(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self,request):
        try :
            user = request.user
            amount = request.data['amount']
            amount = int(amount)*100 # 100rs = 10000 for razorpay api

            # create a order in razorpay
            razorpayOrder = client.order.create({
                                "amount":amount,
                                "currency":"INR",
                                "payment_capture": "1"
                            })
            razorpayOrderStatus = razorpayOrder['status']
            
            if razorpayOrderStatus == 'created':
                razorpayOrderId = razorpayOrder['id']
                
                # add neccesory data to create a payment object
                request.data['razorpay_order_id'] = razorpayOrderId
                request.data['payment_status'] = razorpayOrderStatus
                request.data['user'] = user.id

                # creating a pyament object
                serializer = self.serializer_class(data = request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data,status=status.HTTP_200_OK)
            
            logger.warning('error : razorpay order creation failed!')
            return Response({'error':'razorpay order creation failed!'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class PaymentHandlerViewSet(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self,request):
        try : 
            razorpayOrderId = request.data['razorpay_order_id']
            razorpayPaymentId = request.data['razorpay_payment_id']
            
            payment = Payment.objects.filter(razorpay_order_id = razorpayOrderId)
            if payment.exists():
                payment = payment[0]
                result = client.utility.verify_payment_signature(request.data) # verifying razorpay order id , payment id , signature
                
                if result : # if the payment was successful then it would return None, else it would throw an error.
                    
                    # if razorpay webhook didn't updated the payment status for any reason 
                    # then update the status by calling razorpay api
                    if not payment.is_payment_status_updated :
                        razorpayOrder = client.payment.fetch(razorpayPaymentId)
                     
                        request.data['payment_status'] = razorpayOrder['status']
                        request.data['payment_method'] = razorpayOrder['method']
                        request.data['is_payment_status_updated'] = True
                else :
                    request.data['payment_status'] = PAYMENT_STATUS[3][0] # failed
                    request.data['is_payment_status_updated'] = True
                
                # 'razorpay_payment_signature' would be updated here :
                serializer = self.serializer_class(payment,data=request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                paymentStatus = serializer.data['payment_status']

                # if payment is successfull send a 200 response 
                if paymentStatus == PAYMENT_STATUS[2][0] : # captured
                    return Response(serializer.data,status=status.HTTP_200_OK)
                # else send 400 response
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
            
            logger.warning('error : Please check order id again!')
            return Response({'error':" Please check order id again!"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
