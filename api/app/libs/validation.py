import re
from ipaddress import ip_address
from app.models import model


def a_content_validation(a_content):
    try:
        ip_address(a_content)
    except ValueError:
       return True
    else:
        return False

def mx_content_validation(mx):
    if mx == '@':
        return False
    else:
        pattern = re.compile("^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$")
        if pattern.match(mx):
            return False
        else:
            return True

def cname_content_validation(cname):
    if cname == '@':
        return False
    else:
        pattern = re.compile("^(([a-zA-Z0-9_]|[a-zA-Z_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$")
        if pattern.match(cname):
            return False
        else:
            return True

def txt_content_validation(txt):
    if txt == '@' or txt=='*':
        return False
    else:
        pattern = re.compile("^[\x20-\x7F]*$")
        if pattern.match(txt):
            return False
        else:
            return True

def zone_validation(zone):
    pattern = re.compile("^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$")
    if pattern.match(zone):
        return False
    else:
        return True

def record_validation(record) :
    if record == '@' or record=='*':
        return False
    else:
        pattern = re.compile("^(([\*a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[_A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
        if pattern.match(record):
            return False
        else:
            return True

def count_character(name):
    if name.find("."):
        spl_name = name.split(".")
        total = 0
        for i in spl_name:
            if len(i) >= 64:
                return True
            else:
                total = total + len(i)
        if total >= 255:
            return True
        else:
            return False
    else:
        return False

def record_cname_duplicate(record, types, zone):
    try:
        data_record = model.read_all("record")
    except Exception:
        pass
    else:
        result = False
        for i in data_record:
            type_data = model.read_by_id("type", types)
            if zone == i['zone']:
                if record == i['value'] and type_data['value'] == 'CNAME':
                    result = True
                    break
        return result

def record_mx_duplicate(record, types, zone):
    try:
        data_record = model.read_all("record")
    except Exception as e:
        pass
    else:
        result = False
        for i in data_record:
            type_data = model.read_by_id("type", types)
            if zone == i['zone']:
                if record == i['value'] and type_data['value'] == 'MX':
                    result = True
                    break
        return result


def content_validation(record, content):
    valid = False
    try:
        data_record = model.read_by_id("record", record)
        data_type = model.read_by_id("type", data_record['type'])
    except Exception:
        pass
    else:
        if data_type['value'] == 'A':
            valid = a_content_validation(content)
        elif data_type['value'] == "MX":
            valid = mx_content_validation(content)
        elif data_type['value'] == "CNAME":
            valid = cname_content_validation(content)
        elif data_type['value'] == "TXT":
            valid = txt_content_validation(content)
        else:
            valid = False 
    return valid
    