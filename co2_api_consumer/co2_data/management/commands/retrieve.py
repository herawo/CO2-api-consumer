from django.core.management.base import BaseCommand

from co2_data.api_manager import CO2APIManager

class Command(BaseCommand):
    def handle (self, **options):
        last_import_date = CO2Data.
        data = CO2APIManager.execute(endpoint, method, arguments)