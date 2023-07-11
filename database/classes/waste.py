from django.db import models
from django.utils import timezone

class Waste(models.Model):
    import_datetime = models.DateTimeField(default=timezone.now)
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)