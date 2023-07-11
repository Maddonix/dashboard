from django.db import models
from django.utils import timezone
import pandas as pd
from .center_emissions import (
    ProductEmission,
    ResourceBurntEmission,
    WasteEmission,
    ElectricityUsedEmission,
    ResourceTransportEmission,
    ProductTransportEmission,
)

class EmissionEvaluator(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    center = models.ForeignKey(
        "Center",
        on_delete=models.CASCADE,
        related_name="emission_evaluators"
    )

    # many to many relationship with:
    product_emissions = models.ManyToManyField(
        "ProductEmission",
        related_name="emission_evaluators",
    )
    product_transport_emissions = models.ManyToManyField(
        "ProductTransportEmission",
        related_name="emission_evaluators"
    )
    resource_burnt_emissions = models.ManyToManyField(
        "ResourceBurntEmission",
        related_name="emission_evaluators"
    )
    resource_transport_emissions = models.ManyToManyField(
        "ResourceTransportEmission",
        related_name="emission_evaluators"
    )
    waste_emissions = models.ManyToManyField(
        "WasteEmission",
        related_name="emission_evaluators"
    )
    electricity_used_emissions = models.ManyToManyField(
        "ElectricityUsedEmission",
        related_name="emission_evaluators"
    )

    def __str__(self):
        _str = f"EmissionEvaluator for {self.center.name}"
        # add the values of all emissions
        for emission in self.get_all_emissions():
            substring = f"\n{emission.cause.name} {emission.scope.name} {emission.year}: {emission.emission}"
            _str += substring
        return _str

    def get_emission_attributes(self):
        # returns a list of all emission attributes
        return [
            "product_emissions",
            "product_transport_emissions",
            "resource_burnt_emissions",
            "resource_transport_emissions",
            "waste_emissions",
            "electricity_used_emissions",
        ]

    def get_all_emissions(self):
    # returns a list containing all emissions
        return list(self.product_emissions.all()) + \
            list(self.product_transport_emissions.all()) + \
            list(self.resource_burnt_emissions.all()) + \
            list(self.resource_transport_emissions.all()) + \
            list(self.waste_emissions.all()) + \
            list(self.electricity_used_emissions.all())
    
    def get_emissions_by_cause(self, emissions = None):
        if not emissions:
            emissions = self.get_all_emissions()

        causes = [emission.cause for emission in emissions]
        emissions_by_cause = {}
        for cause in causes:
            emissions_by_cause[cause] = []
        for emission in emissions:
            emissions_by_cause[emission.cause].append(emission)
        return emissions_by_cause
    
    def get_emissions_by_scope(self, emissions = None):
        if not emissions:
            emissions = self.get_all_emissions()
        scopes = [emission.scope for emission in emissions]
        emissions_by_scope = {}
        for scope in scopes:
            emissions_by_scope[scope] = []
        for emission in emissions:
            emissions_by_scope[emission.scope].append(emission)
        return emissions_by_scope

    def get_emissions_by_year(self, emissions = None):
        if not emissions:
            emissions = self.get_all_emissions()
        years = [emission.year for emission in emissions]
        emissions_by_year = {}
        for year in years:
            emissions_by_year[year] = []
        for emission in emissions:
            emissions_by_year[emission.year].append(emission)
        return emissions_by_year
    
    def get_emission_dataframe(self, emissions = None):
        if not emissions:
            emissions = self.get_all_emissions()

        records = []
        for emission in emissions:
            record = emission.record()
            records.append(record)
        # print(record)
        # return records
        emission_dataframe = pd.DataFrame(records)
        # FIXME - little hack to fix nan values in the emission column
        emission_dataframe["emission"] = emission_dataframe["emission"].fillna(0)
        
        # drop rows with emission == 0
        emission_dataframe = emission_dataframe[emission_dataframe["emission"] != 0]
        
        # sort by scope, cause
        emission_dataframe = emission_dataframe.sort_values(by=["scope", "cause"])

        return emission_dataframe