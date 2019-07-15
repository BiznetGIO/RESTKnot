from app import celery
from celery.result import AsyncResult
from app.libs import utils
from app.helpers import command
from app.models import model
from app.helpers import cluster_master, cluster_slave
from app import cs_storage


@celery.task(bind=True)
def get_cluster_data_master(self, id_master):
    res_master = AsyncResult(id=id_master, app=cluster_task_master)
    return res_master

@celery.task(bind=True)
def get_cluster_data_slave(self, id_slave):
    res_slave = AsyncResult(id=id_slave, app=cluster_task_slave)
    return res_slave


@celery.task(bind=True)
def get_cluster_data_master_unset(self, id_master):
    res_master = AsyncResult(id=id_master, app=unset_cluster_master)
    return res_master

@celery.task(bind=True)
def get_cluster_data_slave_unset(self, id_slave):
    res_slave = AsyncResult(id=id_slave, app=unset_cluster_slave)
    return res_slave

@celery.task(bind=True)
def cluster_task_master(self, tags):
    respons = []
    result = []
    id_zone = tags['id_zone']
    master_data = None
    try:
        if cs_storage == 'static':
            master_data = utils.repomaster()
        else:
            master_data = model.get_all("cs_master")
    except Exception as e:
        return str(e)
    else:
        try:
            data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
        except Exception as e:
            print(e)
        for i in master_data:
            print("Execute Master: "+i['nm_master'])
            urls = "http://"+i['ip_master']+":"+i['port']+"/api/command_rest"
            command.conf_begin_http(urls)
            ffi_insert_conf = cluster_master.insert_config_zone(data_zone, i['nm_config'])
            http_response = utils.send_http(urls, ffi_insert_conf)
            result.append(http_response)
            ffi_master = cluster_master.master_create_json_master(data_zone, i['nm_config'])
            http_response = utils.send_http(urls, ffi_master)
            result.append(ffi_master)
            ffi_notify = cluster_master.master_create_json_notify(data_zone, i['nm_config'], urls)
            result.append({'notify':ffi_notify})
            ffi_acl = cluster_master.master_create_json_acl(data_zone, i['nm_config'], urls)
            result.append({"acl": ffi_acl})
            ffi_set_files = cluster_master.set_file_all(data_zone)
            http_response = utils.send_http(urls, ffi_set_files)
            result.append(http_response)
            ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
            http_response = utils.send_http(urls, ffi_set_module)
            result.append(http_response)
            ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
            http_response = utils.send_http(urls, ffi_serial_policy)
            result.append(http_response)
            command.conf_commit_http(urls)
            respons.append({
                "config": i['nm_config'],
                "nm_server": i['nm_master'],
                "data": result
            })
        return respons

@celery.task(bind=True)
def cluster_task_slave(self, tags):
    respons = []
    result = []
    id_zone = tags['id_zone']
    try:
        if cs_storage == 'static':
            slave_data = utils.reposlave()
        else:
            slave_data = model.get_all("v_cs_slave_node")
    except Exception as e:
        return str(e)
    else:
        try:
            data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
        except Exception as e:
            print(e)
        for i in slave_data:
            print("Execute Slave: "+i['nm_slave_node'])
            urls = "http://"+i['ip_slave_node']+":"+i['port_slave_node']+"/api/command_rest"
            command.conf_begin_http(urls)
            ffi_insert_conf = cluster_slave.insert_config_zone(data_zone)
            http_response = utils.send_http(urls, ffi_insert_conf)
            result.append(http_response)
            ffi_slave_master = cluster_slave.master_create_json(data_zone, i['nm_master'])
            http_response = utils.send_http(urls, ffi_slave_master)
            result.append(http_response)
            ffi_slave_acl = cluster_slave.create_json_acl(data_zone, i['nm_master'])
            http_response = utils.send_http(urls, ffi_slave_acl)
            result.append(http_response)
            ffi_set_files = cluster_master.set_file_all(data_zone)
            http_response = utils.send_http(urls, ffi_set_files)
            result.append(http_response)
            ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
            http_response = utils.send_http(urls, ffi_set_module)
            result.append(http_response)
            ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
            http_response = utils.send_http(urls, ffi_serial_policy)
            result.append(http_response)
            command.conf_commit_http(urls)
            respons.append({
                "server": i['nm_config'],
                "data": result
            })
        return respons


@celery.task(bind=True)
def unset_cluster_master(self, tags):
    result = []
    
    id_zone = tags['id_zone']
    try:
        data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    except Exception as e:
        print(e)
    try:
        master_data = model.get_all("cs_master")
    except Exception as e:
        print(e)
    for i in master_data:
        master_command = command.unset_cluster_command_new(tags, data_zone['nm_zone'])
        url_fix= "http://"+i['ip_master']+":"+i['port']
        master_server_url = url_fix+"/api/command_rest"
        command.conf_begin_http(master_server_url)
        http_response_master = utils.send_http(master_server_url, master_command)
        command.conf_commit_http(master_server_url)
        result.append(http_response_master)
    return result

@celery.task(bind=True)
def unset_cluster_slave(self, tags):
    result = []
    
    id_zone = tags['id_zone']
    try:
        data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    except Exception as e:
        print(e)
    try:
        data_slave = model.get_all("v_cs_slave_node")
    except Exception as e:
        print(e)
    for a in data_slave:
        slave_command = command.unset_cluster_command_new(tags, data_zone['nm_zone'])
        url_fix= "http://"+a['ip_slave_node']+":"+a['port_slave_node']
        slave_server_url = url_fix+"/api/command_rest"
        command.conf_begin_http(slave_server_url)
        http_response_slave = utils.send_http(slave_server_url, slave_command)
        command.conf_commit_http(slave_server_url)
        result.append(http_response_slave)
    return result


    