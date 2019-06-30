from app.libs import utils
from app.helpers.rest import response
# from app.models import app_models as db

def parser(json, command=None):
    sdl_endpoint = utils.repodata()
    endpoint = sdl_endpoint['endpoint'][command]
    parameter_fix = list()
    key_query = None
    return_paramfix = list()
    for i in json:
        tagfields=dict()
        for parameters_key in endpoint[i]:
            try:
                parameters_check = json[i][parameters_key]
            except Exception:
                parameters_check = None
            if parameters_check:
                key_query = parameters_key
                data_variabel = dict()
                paramemeters_data = endpoint[i][parameters_key]
                for variabel_key in paramemeters_data: 
                    try:
                        variabel_check = json[i][parameters_key][variabel_key]
                    except Exception:
                        variabel_check = None
                    if variabel_check:
                        data_variabel[variabel_key] = json[i][parameters_key][variabel_key]
                    else:
                        try:
                            data_variabel[variabel_key] = endpoint[i][parameters_key][variabel_key]['default']
                        except Exception as e:
                            return response(401, message=str(e))
                    tagfields[parameters_key]=data_variabel
        parameter=dict()
        for key in tagfields:
            try:
                fields_check = tagfields["fields"]
            except Exception:
                fields_check = None

            try:
                tags_check = tagfields["tags"]
            except Exception:
                tags_check = None

            if fields_check is None and tags_check is not None:
                parameter = {
                    'table': command,
                    'tags' : tagfields['tags']
                }
            elif fields_check is not None and tags_check is None:
                parameter = {
                    'table': command,
                    'fields' : tagfields['fields']
                }
            elif fields_check is not None and tags_check is not None:
                parameter = {
                    'table': command,
                    'fields' : tagfields['fields'],
                    'tags' : tagfields['tags']
                }
            else:
                data = {
                    key_query : tagfields[key]
                }
                parameter = {
                    'table': command,
                    "query" : data,
                }

        parameter_fix.append(parameter)
        return_paramfix = {
            'action': i,
            'data': parameter_fix,
        }
    return return_paramfix


def query_parser(data):
    table = None
    query = None
    data_query = None
    for i in data:
        table = i['table']
        query = i['query']
        for a in query:
            action = a
            data_query = query[a]

    r_query = None
    if a == 'select':
        r_query = select_query(table,data_query)
    elif a == "insert":
        r_query = insert_query(table,data_query)
    else:
        pass

    return r_query

def select_query(table,data):
    query = "select"
    column = None
    where = data['where']
    if type(data['fields']) is list:
        for i in data['fields']:
            if column is None:
                column = i
            else:
                column = column+","+ i
    else:
        column = "*"
    query = query +" "+ column
    if where is None:
        query = query+" from "+table+";"
    else:
        field = where['column']
        value = where['value']
        query = query+" from "+table+" where "+field+"='"+value+"';"
    return query


def insert_query(table,data):
    query = "insert into "+table+""
    column= None
    if type(data['column']['name']) is list:
        query = query +"("
        for i in data['column']['name']:
            if column is None:
                column = i
            else:
                column = column+","+ i
        column = column + ")"
    else:
        column = ""
    query = query + column + " values ("
    values = None
    value = data['values']
    for i in value:
        if values is None:
                values = "'"+value[i]+"'"
        else:
            values = values+",'"+ value[i]+"'"
    query = query +" "+values+")"
    returning = None
    if data['return'] is not None:
        if type(data['return']) is list:
            for i in data['return']:
                if returning is None:
                    returning =  str()
                    returning = i
                else:
                    returning = returning+","+ i
            query = query+" returning " + returning+";"
        else:
            query = query+ " returning " + str(data['return'])+";"
    else:
        query = query+";"
    return query

