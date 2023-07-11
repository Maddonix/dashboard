from django.db import models
from django.utils import timezone

class Material(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    name_german = models.CharField(max_length=255)
    emission_factor = models.ForeignKey('EmissionFactor', on_delete=models.CASCADE, related_name='material')
    emission_factor_import_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()