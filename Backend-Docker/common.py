import hashlib
import json
import logging.config

from dynamic_siddhi_apps.create_app import create_siddhi_config
from dynamic_siddhi_apps.siddhi_admin import SiddhiAdmin

logger = logging.getLogger()
logger.setLevel(logging.INFO)
siddhi_admin = SiddhiAdmin(logger=logger)

def get_channel_name(subscription_message):
    if is_json(subscription_message):
        geographies = []
        commodities = []
        message = json.loads(subscription_message)
        if ('geographies' in message['criteria']):
            geographies = message['criteria']['geographies']
        if ('commodities' in message['criteria']):
            commodities = message['criteria']['commodities']
        cleanmessage = "".join(sorted(geographies) + sorted(commodities))
        print("list:" + cleanmessage)
        encodedmessage = cleanmessage.encode()
        print(encodedmessage)
        cname = hashlib.sha1(encodedmessage).hexdigest()
        return cname
    else:
        return "all"

def create_siddhi_common(message, cname):
    print("Preparing Siddhi App")
    app_name, siddhi_config = create_siddhi_config(json.loads(message), cname, "app")
    print(app_name)
    print(siddhi_config)
    print("Creating Siddhi App")
    siddhi_admin.create_app(siddhi_config)


def is_json(message):
    try:
        json_object = json.loads(message)
    except ValueError as e:
        return False
    return True


def verify_cookie(cookie):
    # TODO: parse a token from the cookie
    logger.info(f'Cookie {cookie}')
    return True

    headers = {
        "Authorization": "Basic Q0lRX1dFQjpQYXNzd29yZDEyMzQ=",
        "x-apigw-api-id": "n8uhmtupi8",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&scope=UserProfile.me&assertion=' + token

    http = urllib3.PoolManager(cert_reqs='CERT_NONE')

    response = http.request('POST',
                            auth_url,
                            body=payload,
                            headers=headers)

    logger.info(response.status)
    import json
    logger.info(json.loads(response.data))
    return response.status == 200







