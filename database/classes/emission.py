from django.db import models
from django.utils import timezone

class Emission(models.Model):
    # center = models.ForeignKey(
    #     "Center",
    #     on_delete=models.CASCADE, 
    #     related_name="emissions"
    # )
    emission = models.FloatField(blank=True, null=True)
    # scope is an integer between 1 and 3
    year = models.IntegerField()
    cause = models.ForeignKey(
        'EmissionCause',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    scope = models.ForeignKey(
        'EmissionScope',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # abstract model
    class Meta:
        abstract = True

    def get_scope(self):
        return self.cause.emission_scope
    
    def record(self):
        record = {
            'emission': self.emission,
            'year': self.year,
            'cause': self.cause.name,
            'scope': self.scope.name,
        }

        # check whether optional fields are present
        # if not, add None to record
        optional_fields = [
            'center',
            'resource',
            'waste',
            "product",
            "transport_step"
        ]

        for field in optional_fields:
            if hasattr(self, field):
                try:
                    record[field] = getattr(self, field)
                    if field == 'transport_step':
                        record[field] = record[field].name
                    elif field == 'center':
                        record[field] = record[field].name
                    elif field == 'resource':
                        record[field] = record[field].resource.name
                    elif field == 'waste':
                        record[field] = record[field].waste.name
                    elif field == 'product':
                        record[field] = record[field]
                except:
                    raise Exception(f"Error in emission record {field}: {record[field]}")
            else:
                record[field] = None

        return record



class EmissionFactor(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    value = models.FloatField()
    unit_import_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('import_datetime', 'import_id',)

class EmissionCause(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name.upper()
    
class EmissionScope(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)

