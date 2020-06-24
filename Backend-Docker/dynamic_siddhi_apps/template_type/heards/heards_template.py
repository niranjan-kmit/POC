__author__ = "ashmeet_kandhari"
__copyright__ = "ashmeet_kandhari"
__license__ = "mit"

import dateutil.parser


def create_request_query(json, headers, connection_id):
    filter_query = create_filter_query(json)
    template_response = create_template_response(json, headers, connection_id)

    return filter_query, template_response


def create_template_response(json, headers, connection_id):
    template_response = f'select  sid, "{connection_id}" as connectionId, sentTime, "{headers},' \
                        f'\'Content-type:application/json\'" as ' \
                        f'headers, str:fillTemplate("""'

    template_response = template_response + '''
 {
    "type": "heards_sub_resp",
    "publishTS": "{{3}}",
    "cepInTS": "{{5}}",
    "processTS": "{{4}}",  
    "headline":"{{1}}",
    "body":"{{2}}",
    "id": "{{6}}",
    "commodities": {{7}},
    "geographies": {{8}},
    "createdDate": "{{9}}",
    "sid":"{{10}}"'''

    if 'correlationId' in json:
        template_response = template_response + """,
    "correlationId":"{{11}}" """
    template_response = template_response + '''
}""", headline, body, ifThenElse(publishTS is null,'null', publishTS), time:timestampInMilliseconds(), 
eventTimestamp(), ifThenElse( id is null, 'null', id), json:toString(commodities), json:toString(geographies), 
str:replaceFirst(createdDate, 'GMT', 'Z'), sid'''

    if 'correlationId' in json:
        correlation_id = json['correlationId']
        template_response = template_response + f", '{correlation_id}') as data"
    else:
        template_response = template_response + ') as data'

    if 'conflationDelivery' not in json:
        json['conflationDelivery'] = "last"

    if 'conflationType' in json and (json['conflationType'] != "C-1" and json['conflationType'] != "-1"):
        if __is_valid_conflation_type(json['conflationType']):
            template_response = template_response + f"\n output {json['conflationDelivery']} every " \
                                                    f"{json['conflationType'][1:]} milliseconds"
        else:
            raise Exception(f"Non supported conflationType {json['conflationType']}")

    return template_response


def create_filter_query(json):
    filter_query = ''
    list_filter_flag = False
    geographies_flag = 'geographies' in json['criteria'] and len(json['criteria']['geographies']) > 0
    commodities_flag = 'commodities' in json['criteria'] and len(json['criteria']['commodities']) > 0

    # TODO enable date filters
    create_date_flag = 'createdDate' in json['criteria'] and (
            "start" in json['criteria']['createdDate'] and json['criteria']['createdDate']['start'])

    if geographies_flag or commodities_flag:
        list_filter_flag = True
        filter_query = __create_list_filter_function(commodities_flag, filter_query, geographies_flag, json)

        if not create_date_flag:
            filter_query += "\n]"

    # TODO Support/ enable date filters
    if create_date_flag:
        filter_query = __create_date_filter_function(filter_query, json, list_filter_flag)

    return filter_query


def __create_list_filter_function(commodities_flag, filter_query, geographies_flag, json):
    filter_query += '[\n'

    if geographies_flag:
        geographies_filter_list_create = 'list:create("' + '", "'.join(json['criteria']['geographies']) + '")'
        geographies_filter = """ifThenElse(list:isList(json:getObject(geographies, '$')), 
            list:size(list:retainAll(json:getObject(geographies, '$'),
            """
        geographies_filter += geographies_filter_list_create + ')) > 0, list:contains(' + \
                              geographies_filter_list_create + \
                              ", cast(json: getObject(geographies, '$'), 'string')))"

        filter_query += geographies_filter

    if commodities_flag:
        if geographies_flag:
            filter_query += "\n\t and \n"
        commodities_filter_list_create = 'list:create("' + '", "'.join(json['criteria']['commodities']) + '")'
        commodities_filter = """ifThenElse(list:isList(json:getObject(commodities, '$')), 
                  list:size(list:retainAll(json:getObject(commodities, '$'),
                  """
        commodities_filter += commodities_filter_list_create + ')) > 0, list:contains(' + \
                              commodities_filter_list_create + \
                              ", cast(json:getObject(commodities, '$'), 'string')))"

        filter_query += commodities_filter
    return filter_query


def __create_date_filter_function(filter_query, json, list_filter_flag):
    if list_filter_flag:
        filter_query += "\n\t and \n"
    else:
        filter_query += '[\n'

    start_date = dateutil.parser.parse(json['criteria']['createdDate']['start'])
    start_date = int(start_date.timestamp() * 1000)

    filter_query += f"\n( math:parseLong('{start_date}') - time:timestampInMilliseconds(createdDate, " \
                    f"\"yyyy-MM-dd'T'HH:mm:ss.SSSZ\") <=0"

    if "end" in json['criteria']['createdDate'] and json['criteria']['createdDate']['end']:
        end_date = dateutil.parser.parse(json['criteria']['createdDate']['end'])
        end_date = int(end_date.timestamp() * 1000)
        filter_query += f" and math:parseLong('{end_date}') - time:timestampInMilliseconds(createdDate, " \
                        f"\"yyyy-MM-dd'T'HH:mm:ss.SSSZ\") >= 0"

    filter_query += ')\n]'
    return filter_query


def __is_valid_conflation_type(conflation_type):
    return conflation_type.startswith('C') and conflation_type[1:].isdigit()
