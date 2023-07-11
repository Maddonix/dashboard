from django.db import models
from django.utils import timezone

# from .unit import Unit
from .product import Product, ProductGroup

class BaseCenterPorperty(models.Model):
    import_id = models.IntegerField(blank=True, null=True)
    center_import_id = models.IntegerField(blank=True, null=True)
    waste_import_id = models.IntegerField(blank=True, null=True)
    product_import_id = models.IntegerField(blank=True, null=True)
    resource_import_id = models.IntegerField(blank=True, null=True)
    unit_import_id = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class Center(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    
    # calculated fields
    total_product_emissions = models.FloatField(blank=True, null=True)
    number_product_groups = models.IntegerField(blank=True, null=True)
    number_products = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()
    
    def get_emission_by_product_group(self, product_group):
        center_products = self.center_products.filter(product__product_group=product_group)
        emission = 0
        for center_product in center_products:
            _emission = center_product.total_emissions
            if _emission:
                emission += _emission
        return emission

    def product_group_emission_dict(self):
        product_groups = ProductGroup.objects.all()
        emission_dict = {}
        for product_group in product_groups:
            emission_dict[product_group.name] = self.get_emission_by_product_group(product_group)
        return emission_dict
    
    def set_number_product_groups(self, save = True):
        self.number_product_groups = self.product_group_emission_dict().__len__()
        if save:
            self.save()

    def set_number_products(self, save = True):
        self.number_products = self.center_products.all().__len__()
        if save:
            self.save()

    def set_total_product_emissions(self, save = True):

        emission_dict = self.product_group_emission_dict()
        total_emissions = 0
        for emission in emission_dict.values():
            total_emissions += emission
        self.total_product_emissions = total_emissions
        if save:
            self.save()

class CenterProduct(BaseCenterPorperty):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    center = models.ForeignKey('Center', on_delete=models.CASCADE, related_name='center_products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='center_products')
    quantity = models.IntegerField(default=0)
    price_per_piece = models.FloatField(blank=True, null=True)
    year = models.IntegerField()
    center_import_id = models.IntegerField(blank=True, null=True)
    product_import_id = models.IntegerField(blank=True, null=True)

    # calculated fields
    total_price = models.FloatField(blank=True, null=True)
    total_emissions = models.FloatField(blank=True, null=True)
    emissions_per_piece = models.FloatField(blank=True, null=True)
    emissions_per_kg = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)


    def __str__(self):
        return f"{self.center.name} - {self.product.name}"
    
    def set_total_price(self, save = True):
        self.total_price = self.quantity * self.price_per_piece
        if save:
            self.save()

    def set_emissions(self, save = True):
        # get product weight in priority
        product: Product = self.product
        product_weight = product.product_weight.get_best_weight()

        product_group = product.product_group
        emission_factor = product_group.reference_product.emission_factor

        if product_weight and emission_factor:
            self.emissions_per_piece = product_weight * emission_factor.value
            self.emissions_per_kg = emission_factor.value
            self.total_emissions = self.quantity * self.emissions_per_piece
            if save:
                self.save()
        
    def calculate_fields(self, save = True):
        self.set_total_price(save = False)
        self.set_emissions(save = False)
        if save:
            self.save()
    
class CenterResource(BaseCenterPorperty):
    center = models.ForeignKey("Center", on_delete=models.CASCADE, related_name="center_resources")
    name = models.CharField(max_length=255)
    center_import_id = models.IntegerField(blank=True, null=True)
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE, related_name="center_resources")
    resource_import_id = models.IntegerField(blank=True, null=True)
    quantity = models.FloatField(verbose_name = "amount")
    use_emission_factor = models.ForeignKey("EmissionFactor", on_delete=models.CASCADE, related_name="center_resource_use")
    use_emission_factor_import_id = models.IntegerField(blank=True, null=True)
    transport_emission_factor = models.ForeignKey("EmissionFactor", on_delete=models.CASCADE, related_name="center_resource_transport")
    transport_emission_factor_import_id = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, related_name="center_resources")
    year = models.IntegerField()

class CenterWaste(BaseCenterPorperty):
    center = models.ForeignKey("Center", on_delete=models.CASCADE, related_name="center_wastes")
    center_import_id = models.IntegerField(blank=True, null=True)
    emission_factor_import_id = models.IntegerField(blank=True, null=True)
    waste_import_id = models.IntegerField(blank=True, null=True)
    waste = models.ForeignKey("Waste", on_delete=models.CASCADE, related_name="center_wastes")
    emission_factor = models.ForeignKey("EmissionFactor", on_delete=models.CASCADE, related_name="center_wastes")
    quantity = models.FloatField(verbose_name = "amount")
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, related_name="center_wastes")
    year = models.IntegerField()


