
from django.db import models
from django.db.models.functions import Extract
from django.db.models import Avg, Count, Min, Sum
from django.db import transaction
from django.db.models import F

from datetime import datetime
from datetime import time


class CO2Data(models.Model):
    rate = models.IntegerField()
    date = models.DateTimeField()

    @classmethod
    def get_last_date(cls):
        if not cls.objects.all().exists():
            return datetime(1000,1,1,0,0)
        return cls.objects.all().order_by('-date').first().date

    def save(self):
        return super(CO2Data, self).save()

    def __str__(self):
        return "{} {}".format(self.rate, self.date)

    def get_frequency_avg(self):
        return CO2DataFrequency.get_avg_at_time(datetime=self.date).get('average_rate')

    @property
    def get_rate_diff(self):
        return CO2DataFrequency.get_avg_at_time(datetime=self.date).get('average_rate') - self.rate

    @classmethod
    def get_avg_days(cls, days):
        data_avg = cls.objects.filter(date__week_day__in=days)
        return data_avg.aggregate(
            calc=(Sum('rate') / Count('rate') )
        ).get('calc')

    @classmethod
    def get_avg_weekend(cls):
        return cls.get_avg_days([2, 3, 4, 5, 6, ])

    @classmethod
    def get_avg_businessday(cls):
        return cls.get_avg_days([1, 7, ])

class CO2DataFrequency(models.Model):
    rate = models.IntegerField()
    time = models.TimeField()
    frequency = models.IntegerField()

    @classmethod
    @transaction.atomic
    def fill_data_frequency(cls):
        frequencies = CO2Data.objects.all().annotate(
            hour=Extract('date', 'hour'),
            minute=Extract('date', 'minute')
        ).values('hour', 'minute', 'rate').annotate(
            count=Count('id')
        ).values('hour', 'minute', 'count', 'rate')
        for freq in frequencies:
            data_time = time(hour=freq.get('hour'), minute=freq.get('minute'))
            cls.objects.create(
                rate=freq.get('rate'),
                time=data_time,
                frequency=freq.get('count')
            )

    def __str__(self):
        return "{} {} {}".format(self.rate, self.time, self.frequency)

    def get_avg_for_same_time(self):
        return self.__class__.get_avg_at_time(time=self.time)

    @classmethod
    def get_avg_at_time(cls, datetime=None, time=None):
        assert datetime or time, "must supply `date` or `datetime` argument"
        if datetime:
            time = datetime.time()
        data_freq = cls.objects.filter(time=time)
        # Calcul d'un moyenne en prenant la fréquence d'un taux sur toutes 
        # les fréquences a cette heure ci
        data_freq = data_freq.annotate(
            calc=(F('frequency') * F('rate') / Sum('frequency') )
        )
        return data_freq.aggregate(average_rate=Avg('calc'))