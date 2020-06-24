def get_siddhi_template(app_name, array_json_path_to_tokenize, scatter_select_query, filter_query, template_response,
                        profile):
    publisher_url = profile['publisher_url']
    kafka_bootstrap_servers = profile['kafka_bootstrap_servers']
    kafka_topic = profile['kafka_topic']

    first_part = f'''@App:name('{app_name}')
@App:description('Description of the plan')


@sink(type = 'http', method = "POST", publisher.url = "{publisher_url}", headers = "{{{{headers}}}}", on.error = 
"LOG", ssl.verification.disabled = "true", 
	@map(type = 'json'))
define stream PricingResponse (headers string, data string);

@source(type = 'kafka', topic.list = "{kafka_topic}", group.id = "{app_name}", threading.option = "topic.wise", 
        bootstrap.servers = "{kafka_bootstrap_servers}", optional.configuration = "auto.offset.reset:latest",
	@map(type = 'json'))
define stream PricingMessage (message string);

@info(name = 'DataPoints-Separator')
from PricingMessage#json:tokenize(message, '{array_json_path_to_tokenize}') 
select {scatter_select_query}, jsonElement as dataPoint, eventTimestamp() as eventTimestamp 
insert into DataPointObj;

'''

    fill_template_part = f'''@info(name = 'Response-Formatter')
from DataPointObj{filter_query}
{template_response}
insert into PricingResponse;
    '''
    return first_part + fill_template_part
