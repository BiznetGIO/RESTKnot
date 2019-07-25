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
            data_commands = list()
            data_commands.append(command.conf_begin_http_cl())
            ffi_insert_conf = cluster_master.insert_config_zone(data_zone, i['nm_config'])
            data_commands.append(ffi_insert_conf)
            ffi_master = cluster_master.master_create_json_master(data_zone, i['nm_config'])
            data_commands.append(ffi_master)
            ffi_notify = None
            ffi_notify = cluster_master.master_create_json_notify(data_zone, i['nm_config'], urls)
            for i_not in ffi_notify:
                data_commands.append(i_not)
            ffi_acl = None
            ffi_acl = cluster_master.master_create_json_acl(data_zone, i['nm_config'], urls)
            for i_ac in ffi_acl:
                data_commands.append(i_ac)
            ffi_set_files = cluster_master.set_file_all(data_zone)
            data_commands.append(ffi_set_files)
            ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
            data_commands.append(ffi_set_module)
            ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
            data_commands.append(ffi_serial_policy)
            data_commands.append(command.conf_commit_http_cl())
            result = utils.send_http_clusters(urls, data_commands)
            respons.append({
                "config": i['nm_config'],
                "nm_server": i['nm_master'],
                "data": result['data'],
                "time": result['times']
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
        data_test = list()
        for i in slave_data:
            print("Execute Slave: "+i['nm_slave_node'])
            urls = "http://"+i['ip_slave_node']+":"+i['port_slave_node']+"/api/command_rest"
            cf_begin = command.conf_begin_http_cl()
            data_test.append(cf_begin)
            ffi_insert_conf = cluster_slave.insert_config_zone(data_zone)
            data_test.append(ffi_insert_conf)
            ffi_slave_master = cluster_slave.master_create_json(data_zone, i['nm_master'])
            data_test.append(ffi_slave_master)
            ffi_slave_acl = cluster_slave.create_json_acl(data_zone, i['nm_master'])
            data_test.append(ffi_slave_acl)
            ffi_set_files = cluster_master.set_file_all(data_zone)
            data_test.append(ffi_set_files)
            ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
            data_test.append(ffi_set_module)
            ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
            data_test.append(ffi_serial_policy)
            cf_commit = command.conf_commit_http_cl()
            data_test.append(cf_commit)
            result = utils.send_http_clusters(urls, data_test)
            respons.append({
                "server": i['nm_config'],
                "data": result['data'],
                "time": result['times']
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
        data = list()
        url_fix= "http://"+i['ip_master']+":"+i['port']
        master_server_url = url_fix+"/api/command_rest"
        data.append(command.conf_begin_http_cl())
        master_command = command.unset_cluster_command_new(tags, data_zone['nm_zone'])
        data.append(master_command)
        command.conf_commit_http_cl()
        response = utils.send_http(master_server_url, data)
        result.append(response)
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
        data_slave = list()
        url_fix= "http://"+a['ip_slave_node']+":"+a['port_slave_node']
        slave_server_url = url_fix+"/api/command_rest"
        data_slave.append(command.conf_begin_http_cl())
        slave_command = command.unset_cluster_command_new(tags, data_zone['nm_zone'])
        data_slave.append(slave_command)
        command.conf_commit_http_cl()
        data_slave.append(command)
        http_response_slave = utils.send_http(slave_server_url, data_slave)
        result.append(http_response_slave)
    return result


    