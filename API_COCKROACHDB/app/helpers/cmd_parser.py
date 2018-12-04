from app.libs import utils
# from app.models import app_models as db

def parser(json, command=None):
    sdl_endpoint = utils.repodata()
    endpoint = sdl_endpoint['endpoint'][command]
    parameter_fix = list()
    return_paramfix = list()
    for i in json:
        tagfields=dict()
        for parameters_key in endpoint[i]:
            try:
                parameters_check = json[i][parameters_key]
            except Exception:
                parameters_check = None
            if parameters_check:
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
                        data_variabel[variabel_key] = endpoint[i][parameters_key][variabel_key]['default']
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
                print("FIELDS NONE")
                parameter = {
                    'table': command,
                    'tags' : tagfields['tags']
                }
            elif fields_check is not None and tags_check is None:
                print("TAGS NONE")
                parameter = {
                    'table': command,
                    'fields' : tagfields['fields']
                }
            elif fields_check is not None and tags_check is not None:
                print("TAGS AND FIELD NOT NONE")
                parameter = {
                    'table': command,
                    'fields' : tagfields['fields'],
                    'tags' : tagfields['tags']
                }
            else:
                print("QUERY EXEC")
                parameter = {
                    'table': command,
                    'fields' : tagfields[key],
                }

        parameter_fix.append(parameter)
        return_paramfix = {
            'action': i,
            'data': parameter_fix,
        }
    print(return_paramfix)
    return return_paramfix

