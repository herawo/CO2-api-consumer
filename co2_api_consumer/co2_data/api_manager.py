import requests
from co2_data.exceptions import RequestException

class CO2APIManager(object):

    URL = 'api-recrutement.ecoco2.com'
    ENDPOINTS = ['v1/data', ]

    @classmethod
    def execute(cls, endpoint, method, arguments=None, data=None, *args, **kwargs):
        if endpoint not in cls.ENDPOINTS:
            raise RequestException("Endpoint not found in class ENDPOINTS")
        call = getattr(requests, method)
        protocol = kwargs.get('protocol', 'https')
        full_endpoint = '{}://{}/{}'.format(protocol, cls.URL, endpoint)
        response = call(
            full_endpoint, params=arguments, data=data, *args, **kwargs
        )
        if response.status_code in range(200, 299):
            return response
        raise response.raise_for_status()