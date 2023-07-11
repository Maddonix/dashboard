from django.db import models
from django.utils import timezone
from .emission import Emission, EmissionFactor
from .unit import Unit

class Product(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    product_group = models.ForeignKey('ProductGroup', on_delete=models.CASCADE, related_name='products')
    product_weight = models.ForeignKey('ProductWeight', on_delete=models.CASCADE)
    emission_factor = models.ForeignKey('EmissionFactor', 
                                        on_delete=models.CASCADE, related_name='product', blank=True, null=True)
    product_group_import_id = models.IntegerField(blank=True, null=True)
    product_weight_import_id = models.IntegerField(blank=True, null=True)

    # TODO should not be saved in db
    materials_str = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()
    
    def set_emission_factor(self):
        # ONLY WORKS FOR PRODUCTS WITH AT LEAST ONE MATERIAL
        # get all product_materials
        product_materials = ProductMaterial.objects.filter(product = self)

        emission = 0
        weight = 0
        for material in product_materials:
            # print(f"{material.name} - {material.material.name} - {material.get_emission()}")
            emission += material.get_emission() # in kg CO2e
            weight += material.get_weight()

        # Create EmissionFactor object
        emission_factor = emission/weight
        emission_factor = EmissionFactor.objects.create(
            unit = Unit.objects.get(name = 'kg'), value = emission)
        self.emission_factor = emission_factor
        self.save()

    def get_materials(self):
        return ProductMaterial.objects.filter(product = self)
    
    def get_materials_string(self):
        product_materials = self.get_materials().all()
        result = "<b>Total Material weight (incl. packaging):</b> " + f"{self.get_total_weight_by_materials(in_g = True)} g<br><br>"
        result += "<b>Materials:<br></b>"
        for _ in product_materials:
            result += f"{_.name.capitalize()} - {_.material.name.capitalize()} - {_.get_weight(in_g = True)} g<br>"

        return result
    
    def set_materials_string(self):
        # if not self._materials_str:
            self.materials_str = self.get_materials_string()
            self.save()

    def get_total_weight_by_materials(self, in_g = False):
        product_materials = self.get_materials().all()
        result = 0
        for _ in product_materials:
            result += _.get_weight(in_g = in_g)
        return result

class ProductGroup(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    reference_product = models.ForeignKey('Product', on_delete=models.CASCADE, null = True, blank = True)
    reference_product_import_id = models.IntegerField(null = True, blank = True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()
    
    def set_reference_product_emission_factor(self):
        reference_product = self.reference_product
        reference_product.set_emission_factor()

    def get_group_emission_factor(self) -> EmissionFactor:
        reference_product = self.reference_product
        return reference_product.emission_factor

class ProductMaterial(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, related_name='products')
    weight_g = models.FloatField()
    product_import_id = models.IntegerField(blank=True, null=True)
    material_import_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()
    
    def get_emission(self):
        # Emission = (material Emission Factor * Weight) / 1000
        return (self.material.emission_factor.value * self.weight_g) / 1000
    
    def get_weight(self, in_g=False):
        """Returns weight in kg"""
        if in_g:
            return self.weight_g
        
        return self.weight_g / 1000

class ProductWeight(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    measured = models.FloatField(null=True, blank=True)
    verified = models.FloatField(null=True, blank=True)
    manufacturer = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def get_best_weight(self):
        "returns best weight in kg"
        if self.verified:
            return self.verified / 1000
        elif self.measured:
            return self.measured / 1000
        elif self.manufacturer:
            return self.manufacturer / 1000
        else:
            return None
        
class ProductTransportStep(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='transport_steps')
    transport_step = models.ForeignKey('TransportStep', on_delete=models.CASCADE, related_name='products')
    product_import_id = models.IntegerField(blank=True, null=True)
    transport_step_import_id = models.IntegerField(blank=True, null=True)
    product_transport_emission = models.ForeignKey('ProductTransportEmission', on_delete=models.CASCADE, related_name='product_transport_steps', null=True, blank=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()
    
