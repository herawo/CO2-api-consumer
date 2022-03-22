from co2_data.models import CO2Data
from django.db import transaction

class CO2ataImporter(object):
    MODEL = CO2Data
    DATA_MATCHING = {
        'co2_rate': {'field_name' : 'rate', },
        'datetime': {'field_name' : 'date', },
    }

    @classmethod
    @transaction.atomic
    def parse_json(cls, json):
        for entry in json:
            cls.import_line(entry)

    @classmethod
    @transaction.atomic
    def import_line(cls, entry):
        new = cls.MODEL()
        for field, field_settings in cls.DATA_MATCHING.items():
            setattr(new, field_settings.get('field_name'), entry.get(field))
        new.save()