from app import celery
from celery.result import AsyncResult
from app.libs import utils
from app.helpers import command
from app.models import model
from app.helpers import cluster_master, cluster_slave


@celery.task(bind=True)
def get_cluster_data_master(self, id_master):
    res_master = AsyncResult(id=id_master, app=cluster_task_master)
    return res_master

@celery.task(bind=True)
def get_cluster_data_slave(self, id_slave):
    res_slave = AsyncResult(id=id_slave, app=cluster_task_slave)
    return res_slave


@celery.task(bind=True)
def cluster_task_master(self, tags):
    respons = []
    result = []
    id_zone = tags['id_zone']
    master_data = model.get_all("cs_master")
    for i in master_data:
        urls = "http://"+i['ip_master']+":"+i['port']+"/api/command_rest"
        command.conf_begin_http(urls)
        ffi_insert_conf = cluster_master.insert_config_zone(id_zone, i['nm_config'])
        http_response = utils.send_http(urls, ffi_insert_conf)
        result.append(http_response)
        ffi_master = cluster_master.master_create_json_master(id_zone, i['nm_config'])
        http_response = utils.send_http(urls, ffi_master)
        result.append(ffi_master)
        ffi_notify = cluster_master.master_create_json_notify(id_zone, i['nm_config'], urls)
        result.append({'notify':ffi_notify})
        ffi_acl = cluster_master.master_create_json_acl(id_zone, i['nm_config'], urls)
        result.append({"acl": ffi_acl})
        ffi_set_files = cluster_master.set_file_all(id_zone)
        http_response = utils.send_http(urls, ffi_set_files)
        result.append(http_response)
        ffi_set_module = cluster_master.set_mods_stats_all(id_zone, "mod-stats/default")
        http_response = utils.send_http(urls, ffi_set_module)
        result.append(http_response)
        ffi_serial_policy = cluster_master.set_serial_policy_all(id_zone, "dateserial")
        http_response = utils.send_http(urls, ffi_serial_policy)
        result.append(http_response)
        command.conf_commit_http(urls)
        respons.append({
            "server": i['nm_config'],
            "data": result
        })
    return respons

@celery.task(bind=True)
def cluster_task_slave(self, tags):
    respons = []
    result = []
    id_zone = tags['id_zone']
    slave_data = model.get_all("v_cs_slave_node")
    for i in slave_data:
        urls = "http://"+i['ip_slave_node']+":"+i['port_slave_node']+"/api/command_rest"
        command.conf_begin_http(urls)
        ffi_insert_conf = cluster_slave.insert_config_zone(id_zone, i['nm_config'])
        http_response = utils.send_http(urls, ffi_insert_conf)
        result.append(http_response)
        ffi_slave_master = cluster_slave.master_create_json(id_zone, i['nm_config'])
        http_response = utils.send_http(urls, ffi_slave_master)
        result.append(http_response)
        ffi_slave_notify = cluster_slave.create_json_notify(id_zone, i['nm_config'], i['nm_slave_node'])
        http_response = utils.send_http(urls, ffi_slave_notify)
        result.append(http_response)
        ffi_slave_acl = cluster_slave.create_json_acl(id_zone, i['nm_config'], i['nm_slave_node'])
        http_response = utils.send_http(urls, ffi_slave_acl)
        result.append(http_response)
        ffi_set_files = cluster_master.set_file_all(id_zone)
        http_response = utils.send_http(urls, ffi_set_files)
        result.append(http_response)
        ffi_set_module = cluster_master.set_mods_stats_all(id_zone, "mod-stats/default")
        http_response = utils.send_http(urls, ffi_set_module)
        result.append(http_response)
        ffi_serial_policy = cluster_master.set_serial_policy_all(id_zone, "dateserial")
        http_response = utils.send_http(urls, ffi_serial_policy)
        result.append(http_response)
        command.conf_commit_http(urls)
        respons.append({
            "server": i['nm_config'],
            "data": result
        })
    return respons
        





    