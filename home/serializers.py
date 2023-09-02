from .models import *
from rest_framework import serializers


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields= ['id','brand_name']

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id','tag']
        
class SubCategorySerializer(serializers.ModelSerializer):
    
    class Meta :
        model = SubCategory
        fields = ['sub_category','category','id']

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta :
        model = Category
        fields = ['id','category','sub_categories']
    
    def get_sub_categories(self,obj):
        subCategories = obj.subcategory_set.all()
        subCategorySerializer = SubCategorySerializer(subCategories,many=True)
        return subCategorySerializer.data
    

class ProductReviewSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = ProductReview
        fields = ['id','user','review','rating']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = SubCategorySerializer()
    tags = ProductTagSerializer(many=True)
    product_review = serializers.SerializerMethodField()
    class Meta :
        model = Product
        fields ='__all__'

    def get_product_review(self,obj):
        ''' getting product's reviews '''
        productReviews = obj.product_review.all()
        serializer = ProductReviewSerializer(productReviews,many=True)
        return serializer.data

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Product
        fields = ['id','name','price','image','discount','rating']