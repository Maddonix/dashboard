from django.db import models
from django.utils import timezone
from .emission import (
    Emission,
    EmissionFactor,
    EmissionCause,
    EmissionScope,
)

class Resource(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('import_datetime', 'import_id',)

    def __str__(self):
        return self.name.upper()



