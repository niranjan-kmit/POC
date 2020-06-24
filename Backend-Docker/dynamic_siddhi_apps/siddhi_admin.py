import logging
import logging.config

import urllib3

try:
    from .app_config import get_heards_profile
except ModuleNotFoundError:
    from src.dynamic_siddhi_apps.app_config import get_heards_profile

# logging
logger = logging.getLogger("urllib3")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

# conf_path = pkg_resources.resource_filename(__name__, os.path.join('resources', 'logging.conf'))
# logging.config.fileConfig(conf_path)

# no request type specific properties needed - either profile is fine
profile = get_heards_profile()

siddhi_manager_url = profile['siddhi_manager_url']
siddhi_request_headers = {
    "accept": "application/json",
    "Content-Type": "text/plain",
    "appkey": "realtime"
}
siddhi_request_headers = {**siddhi_request_headers, **urllib3.util.make_headers(basic_auth='admin:admin')}
http = urllib3.PoolManager(cert_reqs='CERT_NONE')


class SiddhiAdmin(object):
    def __init__(self, logger=None):
        self.__logger = logger or logging.getLogger(__name__)
        self.__http = http

    def create_app(self, payload):
        self.__logger.debug(f'Siddhi payload: {payload}')
        response = self.__http.request('POST',
                                       siddhi_manager_url,
                                       body=payload,
                                       headers=siddhi_request_headers,
                                       timeout=5)
        self.__logger.info(response.status)
        self.__logger.debug(response.data)
        return response

    def update_app(self, payload):
        self.__logger.debug(f'Siddhi payload: {payload}')
        response = self.__http.request('PUT',
                                       siddhi_manager_url,
                                       body=payload,
                                       headers=siddhi_request_headers,
                                       timeout=5)
        self.__logger.info(response.status)
        self.__logger.debug(response.data)
        return response

    def delete_app(self, siddhi_app_id):
        siddhi_delete_url = f'{siddhi_manager_url}/{siddhi_app_id}'
        self.__logger.info(f'Siddhi delete URL: {siddhi_delete_url}')
        response = self.__http.request('DELETE',
                                       siddhi_delete_url,
                                       headers=siddhi_request_headers,
                                       timeout=5)
        self.__logger.info(response.status)
        return response

    def list_apps(self):
        response = self.__http.request('GET',
                                       siddhi_manager_url,
                                       headers=siddhi_request_headers,
                                       retries=False,
                                       timeout=5)
        self.__logger.info(response.status)
        self.__logger.debug(response.data)
        return response
