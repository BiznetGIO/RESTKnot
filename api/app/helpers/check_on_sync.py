from app import celery
from celery.result import AsyncResult
from app.libs import utils
from app.helpers import command
from app.models import model
from app.helpers import cluster_master, cluster_slave
from app import cs_storage
from time import sleep


@celery.task(bind=True)
def get_log_sync_data_master(self, id_master):
    res_master = AsyncResult(id=id_master, app=sync_task_slave)
    return res_master

@celery.task(bind=True)
def get_log_sync_data_slave(self, id_slave):
    res_slave = AsyncResult(id=id_slave, app=sync_task_slave)
    return res_slave

@celery.task(bind=True)
def sync_task_slave(self, data):
    respons = []
    result = []
    data_zone = data['data_zone']
    nm_master = data['nm_master']
    urls = data['urls'] 
    command.conf_begin_http(urls)
    print("BEGIN")
    ffi_insert_conf = cluster_slave.insert_config_zone(data['data_zone'])
    http_response = utils.send_http(urls, ffi_insert_conf)
    result.append(http_response)

    ffi_slave_master = cluster_slave.master_create_json(data_zone, nm_master)
    http_response = utils.send_http(urls, ffi_slave_master)
    result.append(http_response)

    ffi_slave_acl = cluster_slave.create_json_acl(data_zone, nm_master)
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
    print("COMMIT")
    command.conf_commit_http(urls)

    respons.append({
        "data": result
    })
    return respons


@celery.task(bind=True)
def sync_task_master(self, data):
    respons = []
    result = []
    data_zone = data['data_zone']
    urls = data['urls'] 
    sleep(20)
    command.conf_begin_http(urls)
    ffi_insert_conf = cluster_master.insert_config_zone(data_zone, data['nm_config'])
    http_response = utils.send_http(urls, ffi_insert_conf)
    result.append(http_response)
    ffi_master = cluster_master.master_create_json_master(data_zone, data['nm_config'])
    http_response = utils.send_http(urls, ffi_master)
    result.append(ffi_master)
    ffi_notify = cluster_master.master_create_json_notify(data_zone, data['nm_config'], urls)
    result.append({'notify':ffi_notify})
    ffi_acl = cluster_master.master_create_json_acl(data_zone, data['nm_config'], urls)
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
        "config": data['nm_config'],
        "nm_server": data['nm_master'],
        "data": result
    })
    return respons