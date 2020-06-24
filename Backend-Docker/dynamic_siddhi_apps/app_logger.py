import datetime
import logging
import logging.config
from datetime import timezone


def get_utc_timestamp():
    dt = datetime.datetime.now()
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp


class AppLogger(object):
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name or __name__)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - level: TRACE - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)        

    def log_connect_event(self, connection_id):
        utc_timestamp = get_utc_timestamp()

        log = dict()        
        log['utc_ts'] = utc_timestamp
        log['session_id'] = connection_id
        log['source'] = 'ws_api'
        log['event'] = 'on_connect'
        self.logger.info(log)

    def log_message_event(self, connection_id, app_id, request, exec_time = ''):
        utc_timestamp = get_utc_timestamp()

        log = dict()        
        log['utc_ts'] = utc_timestamp
        log['session_id'] = connection_id
        log['app_id'] = app_id
        log['source'] = 'ws_api'
        log['event'] = 'on_message'        
        log['request'] = request
        log['exec_time'] = exec_time
        self.logger.info(log)

    def log_push_event(self, connection_id, app_id, message_id, message_size = ''):
        utc_timestamp = get_utc_timestamp()

        log = dict()        
        log['utc_ts'] = utc_timestamp
        log['session_id'] = connection_id
        log['app_id'] = app_id
        log['message_id'] = message_id
        log['source'] = 'ws_api'
        log['event'] = 'on_push'

        self.logger.info(log)        
    
    def log_delete_app_event(self, connection_id, app_id):
        utc_timestamp = get_utc_timestamp()

        log = dict()        
        log['utc_ts'] = utc_timestamp
        log['session_id'] = connection_id
        log['app_id'] = app_id
        log['source'] = 'ws_api'
        log['event'] = 'on_delete_app'

        self.logger.info(log) 

    def log_disconnect_event(self, connection_id):
        utc_timestamp = get_utc_timestamp()

        log = dict()        
        log['utc_ts'] = utc_timestamp
        log['session_id'] = connection_id
        log['source'] = 'ws_api'
        log['event'] = 'on_disconnect'

        self.logger.info(log)  


