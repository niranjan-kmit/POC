__author__ = "ashmeet_kandhari"
__copyright__ = "ashmeet_kandhari"
__license__ = "mit"


def get_siddhi_template(app_name, filter_query, template_response, connection_id):
    siddhi_sink_in_memory = '@sink(type = "inMemory", topic = "in-memory-output", \n\t@map(type = "json",\n\t\t ' \
                            '@payload("""{"sentTime":{{sentTime}}, "headers":"{{headers}}", "data":{{data}}, ' \
                            '"connectionId":"{{connectionId}}" }""")))'

    siddhi_sink_log = '@sink(type = "log",\n\t' \
                      '@map(type = "json", fail.on.missing.attribute = "false", enclosing.element = "$",\n\t\t' \
                      '@payload("""{"app": "plt-rt", "source":"siddhi-processor", "level": "trace", "event": ' \
                      f'"message_processed", "message_id":{{{{sid}}}},"app_id":"{app_name}" ,' \
                      f'"session_id":"{connection_id}" }}""")))'

    siddhi_source_log = '@sink(type = "log",\n\t' \
                        '@map(type = "json", fail.on.missing.attribute = "false", enclosing.element = "$",\n\t\t' \
                        '@payload("""{"app": "plt-rt", "source":"siddhi-processor", "level": "trace", "event": ' \
                        f'"message_received", "message_id":{{{{sid}}}},"app_id":"{app_name}" ,' \
                        f'"session_id":"{connection_id}" }}""")))'

    first_part = f'''@App:name('{app_name}')
@App:description('Dynamic Heards Filtering Application')

{siddhi_sink_in_memory}
{siddhi_sink_log}
define stream ToInMemoryOutput (sid string, connectionId string, sentTime long, headers string, data string);

@source(type = 'inMemory', topic = "in-memory-input", @map(type = 'passThrough'))
{siddhi_source_log}
define stream FromInMemoryInput (sentTime long, geographies object, commodities object, createdDate string, 
            sid string, headline string, body string, publishTS string, id string);

'''

    fill_template_part = f'''
@info(name = 'Filter Heards Messages')
from FromInMemoryInput{filter_query}
{template_response}
insert into ToInMemoryOutput;
                        '''

    return first_part + fill_template_part
