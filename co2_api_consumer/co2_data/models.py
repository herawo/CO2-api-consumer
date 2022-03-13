
from django.db import models


class CO2Data(models.Model):
    rate = models.IntegerField()
    date = models.DateTimeField()

    @classmethod
    def get_last_date(cls):
        return cls.objects.all().order_by('-date').first().date