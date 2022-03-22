from django.core.management.base import BaseCommand

from co2_data.api_manager import CO2APIManager
from co2_data.importer import CO2ataImporter
from co2_data.models import CO2Data


class Command(BaseCommand):

    help = 'Importe les données CO2 depuis l\'api ecoco2'

    def handle (self, **options):
        last_import_date = CO2Data.get_last_date().timestamp()
        data = {'start': last_import_date}
        data = CO2APIManager.execute('v1/data', 'get', data=data)
        CO2ataImporter.parse_json(data.json())        