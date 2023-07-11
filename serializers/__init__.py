from rest_framework import serializers
from database.models import Product, ProductGroup, Center, ProductMaterial

def get_reference_product_materials(reference_product):
    return ProductMaterial.objects.filter(product=reference_product)

class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        # get all material objects for the reference product

        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    weight = serializers.SerializerMethodField()

    
    class Meta:
        model = Product
        fields = "__all__"
        # fields = [
        #     'name',
        #     'product_group',
        #     'product_weight',
        # ]

    def get_weight(self, obj):
        return obj.product_weight.get_best_weight()


class ProductGroupSerializer(serializers.ModelSerializer):
    reference_product = ProductSerializer(read_only=True)
    # get all product materials for the reference product
    product_materials = ProductMaterialSerializer(many=True, read_only=True)

    reference_product_name = serializers.CharField(source='reference_product.name', read_only=True)
    reference_product_weight_incl_packaging = serializers.CharField(source='reference_product.product_weight.verified', read_only=True)

    # get all material objects for the reference product
    reference_product_materials = serializers.SerializerMethodField()
    reference_product_material_tuples = serializers.SerializerMethodField()
    # reference_product_material_string = serializers.CharField(
    #     source='reference_product.get_materials_string', read_only=True
    # )

    class Meta:
        model = ProductGroup
        # fields = "__all__"
        fields = [
            "pk",
            'name', 
            "reference_product_name",
            "reference_product",
            "product_materials",
            "reference_product_weight_incl_packaging",
            "reference_product_materials",
            "reference_product_material_tuples",
            # "reference_product_material_string",
        ]

    def get_reference_product_materials(self, obj, as_str_list=True):
        if obj.reference_product:
            materials = ProductMaterial.objects.filter(product=obj.reference_product)
            if as_str_list:
                return [f"<br>    {material.material.name} ({material.weight_g}g)" for material in materials]
            else:
                return ProductMaterialSerializer(materials, many=True).data
        return None
    
    def get_reference_product_material_tuples(self, obj):
        if obj.reference_product:
            materials = ProductMaterial.objects.filter(product=obj.reference_product)
            return [(material.material.name, material.weight_g) for material in materials]
        return None

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = "__all__"
