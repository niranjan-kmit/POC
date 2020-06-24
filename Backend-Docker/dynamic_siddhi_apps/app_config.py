import configparser
import os

import pkg_resources

# init environment variable
if 'WS_ENV' in os.environ:
    ENV = os.environ['WS_ENV'].strip().lower()
else:
    ENV = 'sandbox'

# parse configuration based on the environment
config = configparser.ConfigParser()
config_file = 'properties-' + ENV + '.ini'
config_file_path = pkg_resources.resource_filename(__name__, os.path.join('resources', config_file))
config.read(config_file_path)


def get_pricing_profile():
    return config['PRICING']


def get_heards_profile():
    return config['HEARDS']
