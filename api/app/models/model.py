from app import etcd_client as client
from etcd import EtcdKeyNotFound
from etcd import EtcdException
import ast, json


def insert_data(stored, key, data):
    try:
        data = client.write("/"+stored+"/"+key, data)
    except EtcdException as e:
        raise e
    else:
        return data.key

def delete(stored, key):
    try:
        b = client.delete("/"+stored+"/"+key, recursive=True, dir=True)
    except EtcdException as e:
        raise e
    else:
        return b.key

def read_by_id(stored, key):
    try:
        a = client.read("/"+stored+"/"+key)
    except EtcdKeyNotFound as e:
        raise e
    else:
        data = ast.literal_eval(a.value)
        return data

def read_all(stored):
    result = list()
    try:
        a = client.read("/"+stored)
    except EtcdKeyNotFound as e:
        raise e
    else:
        for child in a.children:
            data = ast.literal_eval(child.value)
            result.append(data)
    return result

def check_relation(stored, key):
    try:
        read_by_id(stored, key)
    except Exception as e:
        return True
    else:
        return False

def read_all_key(stored):
    result = list()
    try:
        a = client.read("/"+stored)
    except EtcdKeyNotFound as e:
        raise e
    else:
        for child in a.children:
            data = ast.literal_eval(child.value)
            result.append(int(data['key']))
    return result

def update(stored, key, data):
    try:
        delete(stored, str(key))
    except Exception as e:
        raise e
    try:
        data = insert_data(stored, key, data)
    except Exception as e:
        raise e
    else:
        return data

def content_by_record(record):
    data = list()
    try:
        content_data = read_all("content")
    except Exception as e:
        raise e
    else:
        for i in content_data:
            if i['record'] == record:
                data.append(i)
    return data

def serial_by_record(record):
    result = list()
    try:
        content_data = read_all("serial")
    except Exception as e:
        raise e
    else:
        for i in content_data:
            if i['record'] == record:
                result.append(i)
    return result


def record_by_zone(zone):
    result = list()
    try:
        data_rec = read_all("record")
    except Exception:
        data_rec = []
    else:
        for i in data_rec:
            data = None
            if i['zone'] == zone:
                type_data = read_by_id("type", i['type'])
                ttl_data = read_by_id("ttl", i['ttl'])
                try:
                    content_data = content_by_record(i['key'])
                except Exception:
                    content_data = []
                if i['serial']:
                    try:
                        serial_data = serial_by_record(i['key'])
                    except Exception:
                        data = {
                            "key": i['key'],
                            "value": i['value'],
                            "created_at": i['created_at'],
                            "type": type_data,
                            "ttl": ttl_data,
                            "content": content_data,
                            "serial": []
                        }
                    else:
                        data = {
                            "key": i['key'],
                            "value": i['value'],
                            "created_at": i['created_at'],
                            "type": type_data,
                            "ttl": ttl_data,
                            "content": content_data,
                            "serial": serial_data
                        }
                else:
                    data = {
                        "key": i['key'],
                        "value": i['value'],
                        "created_at": i['created_at'],
                        "type": type_data,
                        "ttl": ttl_data,
                        "content": content_data
                    }
            if data is not None:
                result.append(data)
        return result


def record_delete(key):
    try:
        record_data = read_by_id("record", key)
    except Exception as e:
        raise e
    else:
        try:
            conten_data = content_by_record(key)
        except Exception as e:
            print(e)
        else:
            for ci in conten_data:
                if record_data['serial']:
                    serial_data = serial_by_record(key)
                    for i in serial_data:
                        try:
                            delete("serial", i['key'])
                        except Exception as e:
                            raise e
                try:
                    delete("content", ci['key'])
                except Exception as e:
                    print(e)
        try:
            result = delete("record", key)
        except Exception as e:
            raise e
        else:
            return result

def get_user_by_project_id(project_id):
    try:
        data_user = read_all("user")
    except Exception as e:
        raise e
    else:
        data = {}
        for i in data_user:
            if i['project_id'] == project_id:
                data = i
                break
        return data
        
        
