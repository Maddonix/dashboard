from django.db import models
from django.utils import timezone

class TransportStep(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    emission_factor = models.ForeignKey('EmissionFactor', on_delete=models.CASCADE, related_name='transport_steps')
    emission_factor_import_id = models.IntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, blank=True, null=True)
    unit_import_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()

    def get_emission(self):
        # Emission = (material Emission Factor * Weight) / 1000
        return (self.emission_factor.value * self.weight_g) / 1000

    def get_weight(self, in_g=False):
        """Returns weight in kg"""
        if in_g:
            return self.weight_g
        
        return self.weight_g / 1000
