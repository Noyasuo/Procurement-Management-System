from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from pms_api.serializer import ProductSerializer, CategorySerializer
from core.models import Product, Category


@extend_schema(tags=["Product"])
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # Get the category name from the validated data
        category_name = serializer.validated_data.get('category', {}).get('name', None)
        
        if category_name:
            # Check if the category exists, create it if not
            category, created = Category.objects.get_or_create(name=category_name)
        else:
            category, created = Category.objects.get_or_create(name="No Category")

        product = serializer.save(category=category)
        product.user = self.request.user
        product.save()
        
        # Optionally, you can return a custom response if needed, or the default will apply
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Product"])
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@extend_schema(tags=["Category"])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(tags=["Category"])
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
