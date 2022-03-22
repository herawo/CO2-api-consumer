from django.core.management.base import BaseCommand

from co2_data.models import CO2DataFrequency


class Command(BaseCommand):

    help = 'Traduit les données de CO2Data vers CO2DataFrequency'

    def handle (self, **options):
        CO2DataFrequency.fill_data_frequency()   