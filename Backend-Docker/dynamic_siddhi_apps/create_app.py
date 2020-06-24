import logging

# this is a temp fix we need to see if there is a better way to fix this
try:
    from .template_type.pricing.siddhi_template import get_siddhi_template as pricing_siddhi_template
    from .template_type.pricing import pricing_template
    from .template_type.heards.siddhi_template import get_siddhi_template as heards_siddhi_template
    from .template_type.heards import heards_template
    from .app_config import get_heards_profile, get_pricing_profile
except ModuleNotFoundError:
    from dynamic_siddhi_apps.template_type.pricing.siddhi_template import \
        get_siddhi_template as pricing_siddhi_template
    from dynamic_siddhi_apps.template_type.heards.siddhi_template import \
        get_siddhi_template as heards_siddhi_template
    from dynamic_siddhi_apps.template_type.pricing import pricing_template
    from dynamic_siddhi_apps.template_type.heards import heards_template
    from dynamic_siddhi_apps.app_config import get_heards_profile, get_pricing_profile

__author__ = "ashmeet_kandhari"
__copyright__ = "ashmeet_kandhari"
__license__ = "mit"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_heards_filters(json):
    return ('commodities' not in json or len(json['commodities']) == 0) and (
            'geographies' not in json or len(json['geographies']) == 0) and (
                   'createdDate' not in json or 'start' not in json['createdDate'] or
                   'end' not in json['createdDate'])
    pass


def create_query(json, headers, app_name, disable_filters, connection_id):
    if json['type'] == 'pricing_req':
        array_json_path_to_tokenize, scatter_select_query, select_query, filter_query, template_response = \
            pricing_template.create_request_query(json, headers)

        if not disable_filters:
            if len(json['item']['symbols']) == 0:
                return ''
        else:
            filter_query = ''

        pricing_profile = get_pricing_profile()
        return pricing_siddhi_template(app_name, array_json_path_to_tokenize, scatter_select_query,
                                       filter_query, template_response, pricing_profile)

    if json['type'] == 'heards_sub_req':
        filter_query, template_response = heards_template.create_request_query(json, headers, connection_id)
        if not disable_filters:
            if ('criteria' not in json or len(json['criteria']) == 0 or check_heards_filters(
                    json['criteria'])):
                return ''
        else:
            filter_query, filter_query_function = '', ''

        return heards_siddhi_template(app_name, filter_query, template_response, connection_id)

    return ""


def validate_input(input):
    return True
    pass


def create_siddhi_config(json_req, connection_id, app_key, disable_filters=False):
    # app_name = hashlib.md5((connectionId + "_" + json_req['type']).encode('utf-8')).hexdigest()
    if validate_input(json_req):
        app_name = (connection_id + "_" + json_req['type'])
        headers = f"'connectionId:{connection_id}',{app_key}"
        siddhi_config = create_query(json_req, headers, app_name, disable_filters, connection_id)
        if not siddhi_config:
            return '', ''
        return app_name, siddhi_config
    raise ValueError('Please check the subscription json')


if __name__ == '__main__':
    connectionId = "test_connectionId"
    app_key = "'appKey:workManWork'"
    pricing_json_req = {
        "type": "pricing_req",
        "conflationDelivery": "first",
        "conflationType": "C200",
        "item": {
            "symbols": [],
            "fields": []
        },
        "correlationId": "15",
        "source": "PLATTS"
    }

    heards_json_req = {
        "type": "heards_sub_req",
        "conflationDelivery": "first",
        "conflationType": "C5",
        "criteria": {
            "commodities": ["Utilities"],
            "geographies": ["Europe", "Asia"],
            "createdDate": {
                "start": "2020-04-09T00:00:00.000Z",
                "end": "2020-04-13T23:59:59.000Z"
            }

        },
        "correlationId": "Test123",
        "source": "PLATTS"
    }

    name, siddhi_config = create_siddhi_config(heards_json_req, connectionId, app_key, False)
    print(name)
    print(siddhi_config)

    # logger = logging.getLogger(__name__)
    # from siddhi_admin import SiddhiAdmin
    #
    # # logger.setLevel(logging.DEBUG)
    # siddhi_admin = SiddhiAdmin()
    # siddhi_admin.list_apps()
