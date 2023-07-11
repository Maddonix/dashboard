from django.db import models
from django.utils import timezone
from .emission import (
    Emission,
)

class ProductEmission(Emission):
    product = models.ForeignKey('Product', related_name='product_emissions', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=255)
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="product_emissions"
    )
    ## seems to be implemented not in the best way, but it works
    ## complicated to change because of ProductEmission is calculated for one product
    ## but then referenced by the product group
    product = models.CharField(max_length=255)
    product_quantity = models.FloatField(null=True, blank=True)
    product_weight = models.FloatField(null=True, blank=True)
    emission_per_product = models.FloatField(null=True, blank=True)

    # combination of center, product and year must be unique
    class Meta:
        unique_together = ('center', 'product', 'year',)

    # has inherited method get_scope from Emission

class ResourceBurntEmission(Emission):
    # inherits the following fields from Emission:
    # emission = models.FloatField(blank=True, null=True)
    # year = models.IntegerField()
    # cause = models.ForeignKey('EmissionCause')
    # scope = models.ForeignKey('EmissionScope')
    # center = models.ForeignKey('Center')
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="burnt_emissions"
        )
    resource = models.ForeignKey(
        "CenterResource",
        on_delete=models.CASCADE, 
        related_name="burnt_emissions"
    )

class WasteEmission(Emission):
    waste = models.ForeignKey('CenterWaste', related_name='waste_emissions', on_delete=models.CASCADE)
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="waste_emissions"
        )
    # combination of center, waste and year must be unique
    class Meta:
        unique_together = ('center', 'waste', 'year',)

    # has inherited method get_scope from Emission

class ElectricityUsedEmission(Emission):
    # inherits the following fields from Emission:
    # emission = models.FloatField(blank=True, null=True)
    # year = models.IntegerField()
    # cause = models.ForeignKey('EmissionCause')
    # scope = models.ForeignKey('EmissionScope')
    # center = models.ForeignKey('Center')
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="electricity_used_emissions"
        )
    resource = models.ForeignKey("CenterResource", on_delete=models.CASCADE, related_name="electricity_used_emissions")


    # combination of center, year and cause must be unique

class ResourceTransportEmission(Emission):
    # inherits the following fields from Emission:
    # emission = models.FloatField(blank=True, null=True)
    # year = models.IntegerField()
    # cause = models.ForeignKey('EmissionCause')
    # scope = models.ForeignKey('EmissionScope')
    # center = models.ForeignKey('Center')
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="resource_transport_emissions"
        )
    resource = models.ForeignKey("CenterResource", on_delete=models.CASCADE, related_name="transport_emissions")

class ProductTransportEmission(Emission):
    # inherits the following fields from Emission:
    # emission = models.FloatField(blank=True, null=True)
    # year = models.IntegerField()
    # cause = models.ForeignKey('EmissionCause')
    # scope = models.ForeignKey('EmissionScope')
    # center = models.ForeignKey('Center')
    product = models.ForeignKey('CenterProduct', related_name='product_transport_emissions', on_delete=models.CASCADE)
    center = models.ForeignKey(
        "Center", on_delete=models.CASCADE,
        related_name="product_transport_emissions"
    )
    transport_step = models.ForeignKey('TransportStep', related_name='product_transport_emissions', on_delete=models.CASCADE, blank=True, null=True)
    # combination of center, product and year must be unique
    class Meta:
        unique_together = ('center', 'product', 'year',)

    # has inherited method get_scope from Emission
