from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from database.models import ProductGroup, Center, Product
from serializers import ProductGroupSerializer, CenterSerializer, ProductSerializer

def get_product_group_details(request):
    product_group_id = request.GET.get('id', None)
    product_group = get_object_or_404(ProductGroup, id=product_group_id)

    serializer = ProductGroupSerializer(product_group)
    
    return JsonResponse(serializer.data, safe=False)


def get_center_details(request):
    center_id = request.GET.get('id', None)
    center = get_object_or_404(Center, id=center_id)
    serializer = CenterSerializer(center)
    return JsonResponse(serializer.data, safe=False)


def product_data(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data)