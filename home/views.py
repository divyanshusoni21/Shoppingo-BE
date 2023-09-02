from .models import *
from .serializers import *

from shoppingo.settings import logger
import traceback

from rest_framework.response import Response
from rest_framework import status,generics,viewsets

class ProductViewSet(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ProductDetailSerializer

    def get(self,request,productId):
        ''' return a detailed info of product.'''
        try :
            # get product with it's related and reverse related objects like brand,tags,category and reviews
            product = Product.objects.filter(id = productId).select_related().prefetch_related('product_review')
            if product.exists():
                product = product[0]
                serializer = self.serializer_class(product,context={"request": request})
                return Response(serializer.data,status=status.HTTP_200_OK)
            logger.warning('error : No product found with given id!')
            return Response({'error':'No product found with given id!'},status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        ''' return all categories with their sub categories'''
        try : 
            categories = Category.objects.all().prefetch_related('subcategory_set')
            serializer = self.serializer_class(categories,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        '''return all products associated with a sub category'''
        try :
            categoryId = kwargs['pk']
            # get sub category with products associated with it
            subCategory = SubCategory.objects.filter(id = categoryId).prefetch_related('product_set')
            if subCategory.exists():
                subCategory = subCategory[0]
                products = subCategory.product_set.all() # getting the products
                serializer = ProductSerializer(products,many=True,context={"request": request})
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            logger.warning('error : Please check category id again!')
            return Response({'error':'Please check category id again!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
       


