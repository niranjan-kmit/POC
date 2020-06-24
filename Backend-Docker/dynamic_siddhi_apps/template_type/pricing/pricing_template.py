def create_request_query(json, headers):
    fields_list = ["publishTS", "sendTo", "service"]
    select_query = ", ".join(fields_list)
    array_json_path_to_tokenize = "$.num.dataPoint"

    scatter_select_query = create_scatter_query(fields_list)

    filter_query = create_filter_query(json)

    template_response = create_template_response(json, headers)

    return array_json_path_to_tokenize, scatter_select_query, select_query, filter_query, template_response


def create_template_response(json, headers):
    template_response = f'select  "{headers}" as headers, str:fillTemplate("""'
    template_response = template_response + '''
 {
    "message": {
    "publishTS": "{{3}}",
    "cepInTS": "{{5}}",
    "processTS": "{{4}}",  
    "service":{{1}},
    "dataPoint":{{2}}
 }
}""", service, dataPoint, publishTS, time:timestampInMilliseconds(), eventTimestamp) as data '''

    if 'conflationDelivery' not in json:
        json['conflationDelivery'] = "last"

    if 'conflationType' in json and (json['conflationType'] != "C-1" and json['conflationType'] != "-1"):
        if __is_valid_conflation_type(json['conflationType']):
            template_response = template_response + f"\n output {json['conflationDelivery']} every {json['conflationType'][1:]} milliseconds"
        else:
            raise Exception(f"Non supported conflationType {json['conflationType']}")

    return template_response


def create_filter_query(json):
    filter_query = ''
    if len(json['item']['symbols']) > 0:
        filter_query = '['
        if len(filter_query) > 1:
            filter_query = filter_query + " and"
        filter_query = filter_query + " (json:getString(dataPoint, '$.symbol') =='" + \
                       "' or json:getString(dataPoint, '$.symbol') == '".join(
                           json['item']['symbols']) + "')"
        filter_query = filter_query + "]"

    return filter_query


def create_scatter_query(fields_list):
    # f"'{json['correlationId']}'"
    scatter_select_query = ""
    for field in fields_list:
        scatter_select_query = scatter_select_query + f"json:getString(message, '$.{field}') as {field}, "
    scatter_select_query = scatter_select_query[:-2]
    return scatter_select_query


def __is_valid_conflation_type(conflation_type):
    return conflation_type.startswith('C') and conflation_type[1:].isdigit()
