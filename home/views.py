from .models import *
from order.models import OrderItem,ORDER_STATUS

from .serializers import *

from utility.pagination import StandardResultsSetPagination
from shoppingo.settings import logger
import traceback

from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
from django.db.models import Q

class ProductViewSet(generics.GenericAPIView):

    serializer_class = ProductDetailSerializer

    def get(self,request,productSlug):
        ''' return a detailed info of product.'''
        try :
            # get product with it's related and reverse related objects like brand,tags,category and reviews
            product = Product.objects.filter(slug = productSlug).select_related('brand','category').prefetch_related('product_review','tags')
            if not product.exists():
                raise Exception('error : No product found with given id!')
            
            product = product[0]
            serializer = self.serializer_class(product,context={"request": request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
 
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        ''' return all categories with their sub categories'''
        try : 
            categories = Category.objects.prefetch_related('subcategory_set')
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
            if not subCategory.exists():
                raise Exception('error : Please check category id again!')
            
            subCategory = subCategory[0]
            products = subCategory.product_set.all() # getting the products
            
            # paginating the products
            page = self.paginate_queryset(products)
            if page is not None:
                # serialize the page 
                serializer = ProductSerializer(page,many = True,context={'request':request})
               
                return self.get_paginated_response(serializer.data)
            
            serializer = ProductSerializer(products,many=True,context={"request": request})
            return Response(serializer.data,status=status.HTTP_200_OK)
            
            
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
       
class UserCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserCart.objects.all()
    serializer_class = userCartSerializer

    
    def list(self,request,*args,**kwargs):
        try : 
            user = request.user
            # get all the products of user has in the cart.
            userCart = UserCart.objects.filter(user = user,quantity__gt = 0).select_related()
            # using diffrent serializer to get product data as well
            serializer = userCartGetSerializer(userCart,many=True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        try :
            user = request.user
            productId = request.data['product']
            quantity = request.data['quantity']

            product = Product.objects.filter(id = productId)
            if not product.exists():
                raise Exception('error : Check product id again!')
                
            product = product[0]

            # handleing edge case : if any object in UserCart is already there for that product then increase the quantity
            cart = UserCart.objects.filter(user = user , product=product)
            if cart.exists():
                cart = cart[0]
                cart.quantity = int(quantity)
            else :
                # create a new object
                cart = UserCart(user = user, 
                                product = product,
                                quantity = int(quantity)
                            )
            cart.save() 
            return Response({'success':'cart created successfully'},status=status.HTTP_200_OK)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        try : 
            productId = kwargs['pk']
            user = request.user
            quantity = int(request.data['quantity'])
            cartItem = UserCart.objects.filter(product_id=productId,user = user)
            if not  cartItem.exists():
                raise Exception('error : Please check product id again!')
            
            cartItem = cartItem[0]
            
            # handling the edge case : if quantity provided is 0 , delete the object
            if quantity == 0 :
                cartItem.delete()
            else :
                # update the quantity for the product
                cartItem.quantity = quantity
                cartItem.save()

            return Response({'success':'cart updated successfully'},status=status.HTTP_200_OK)
            
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try :
            productId = kwargs['pk']
            user = request.user
            cartItem = UserCart.objects.filter(product_id=productId,user = user)
            if not cartItem.exists():
                raise Exception('please check product id again!')
            
            cartItem = cartItem[0]
            cartItem.delete()
            return Response({'success':'deleted cart item'},status=status.HTTP_200_OK)
            
        
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
       

class ProductReviewViewSet(generics.GenericAPIView):
    serializer_class = ProductReviewSerializer

    def post(self,request):
        try :
            user = request.user
            productId = request.data['product']
            product = Product.objects.filter(id = productId)
            if not product.exists():
                raise Exception('error : please check product id again!')
            
            product = product[0]
            # only let the user the to review the product if he/she has used it
            userOrder = OrderItem.objects.filter(order__user = user , order__order_status = ORDER_STATUS[2][0] , product = product)
            if not userOrder.exists():
                raise Exception('error : user have not used this product yet!')
            
            # if any order exists save the review
            request.data['user'] = user.id
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success':'Product review posted'},status=status.HTTP_200_OK)
            
                 
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class SearchViewSet(generics.GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get(self,request,query):
        ''' get products by searching name , category or brand name '''
        try :
            # search the query product name , sub-category and brand name
            productsByName = Product.objects.filter(name__icontains = query)
            productsByCategory = Product.objects.filter(category__sub_category__icontains = query)
            productsByBrand = Product.objects.filter(brand__brand_name__icontains = query)

            # merge all the results 
            allProducts = productsByName.union(productsByCategory,productsByBrand) # By default, union() removes duplicates from the result.

            # paginating the products
            page = self.paginate_queryset(allProducts)
            if page is not None:
                # serialize the page 
                serializer = self.serializer_class(page,many = True,context={'request':request})
               
                return self.get_paginated_response(serializer.data)
            
            serializer = self.serializer_class(allProducts,many=True,context={"request": request})
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
