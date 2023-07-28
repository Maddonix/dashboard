from django.db import models

class Unit(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Waste(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class EmissionCause(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class EmissionFactor(models.Model):
    import_id = models.AutoField(primary_key=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    value = models.FloatField()

class EmissionScope(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Manufacturer(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)

class Material(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    name_german = models.CharField(max_length=255, null=True)
    emission_factor = models.ForeignKey("EmissionFactor", on_delete=models.SET_NULL, null=True)

class ProductMaterial(models.Model):
    import_id = models.IntegerField(primary_key=True)
    component = models.CharField(max_length=255)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    product = models.ForeignKey('ProductCatalogue', on_delete=models.CASCADE)
    weight = models.FloatField(null=True)

class Resource(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

import numpy as np
import pandas as pd
class ProductWeight(models.Model):
    import_id = models.IntegerField(primary_key=True)
    measured = models.FloatField(null=True)
    verified = models.FloatField(null=True)
    manufacturer = models.FloatField(null=True)

    def get_weight(self):
        if not pd.isnull(self.verified):
            return self.verified
        elif not pd.isnull(self.measured):
            return self.measured
        elif not pd.isnull(self.manufacturer):
            return self.manufacturer
        else:
            return None

class ProductGroup(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    reference_product = models.ForeignKey('ProductCatalogue', on_delete=models.SET_NULL, null=True)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.SET_NULL, null=True)

    def get_emission_factor(self):
        if self.emission_factor:
            return self.emission_factor

        else:
            assert self.reference_product, "No reference product set for product group {}".format(self.name)
            product = self.reference_product
            materials = ProductMaterial.objects.filter(product=product)
            emission = 0
            weight = 0
            for material in materials:
                emission += material.material.emission_factor.value * material.weight
                weight += material.weight
            emission_factor = emission / weight

            # Create new emission factor unit is kg, this has id == 1
            emission_factor_unit = Unit.objects.get(pk=1)
            i = 0
            while i <99:
                try: 
                    emission_factor = EmissionFactor.objects.create(unit=emission_factor_unit, value=emission_factor)
                except:
                    print("Emission factor already exists, trying again")
                    pass

                i+= 1
            self.emission_factor = emission_factor
            self.save()

            return emission_factor

class ProductCatalogue(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    manufacturer_product_id = models.CharField(max_length=255, null=True)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.SET_NULL, null=True)
    product_weight = models.ForeignKey(ProductWeight, on_delete=models.SET_NULL, null=True)
    name_clean = models.CharField(max_length=255, null = True)
    old_import_id = models.FloatField(null=True)
    old_name = models.CharField(max_length=255, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null = True)


class CenterProduct(models.Model):
    center_product_doc_id = models.IntegerField(null = True)
    product_doc_runnning_id = models.IntegerField(null=True)
    department_id = models.IntegerField(null=True)
    product = models.ForeignKey(ProductCatalogue, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255, null=True)
    date = models.DateTimeField()
    price = models.FloatField(null = True)
    product_group_intern = models.CharField(max_length=255, null=True)
    center = models.ForeignKey('Center', on_delete=models.CASCADE)

    # function to get the product group of the product
    def get_product_group(self):
        return self.product.product_group
    
    # function to get the product weight of the product
    def get_product_weight(self):
        return self.product.product_weight
    
    # function to get the emission factor of the product
    def get_emission_factor(self):
        return self.product.product_group.emission_factor

class CenterProducts(models.Model):
    center = models.ForeignKey('Center', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductCatalogue, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    weight_per_product = models.FloatField()
    reference_emission_per_weight = models.FloatField()
    total_emission = models.FloatField()
    year = models.IntegerField()

    # the combination of center + year + product should be unique
    class Meta:
        unique_together = ('center', 'year', 'product')

class CenterResource(models.Model):
    import_id = models.IntegerField(primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    use_emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE, related_name='use_emission_factors')
    transport_emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE, related_name='transport_emission_factors')
    year = models.IntegerField()
    center = models.ForeignKey('Center', on_delete=models.CASCADE)

class CenterWaste(models.Model):
    import_id = models.IntegerField(primary_key=True)
    center = models.ForeignKey('Center', on_delete=models.CASCADE)
    waste = models.ForeignKey(Waste, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE)
    year = models.IntegerField()

class TransportStep(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    distance = models.IntegerField()
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

class Center(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
