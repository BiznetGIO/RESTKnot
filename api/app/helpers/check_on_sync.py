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
    
    result.append(command.conf_begin_http_cl())
    ffi_insert_conf = cluster_slave.insert_config_zone(data['data_zone'])
    result.append(ffi_insert_conf)
    ffi_slave_master = cluster_slave.master_create_json(data_zone, nm_master)
    result.append(ffi_slave_master)
    ffi_slave_acl = cluster_slave.create_json_acl(data_zone, nm_master)
    result.append(ffi_slave_acl)
    ffi_set_files = cluster_master.set_file_all(data_zone)
    result.append(ffi_set_files)
    ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
    result.append(ffi_set_module)
    ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
    result.append(ffi_serial_policy)
    result.append(command.conf_commit_http_cl())
    data_res = utils.send_http_clusters(urls, result)
    respons.append({
        "data": data_res
    })
    return respons


@celery.task(bind=True)
def sync_task_master(self, data):
    respons = []
    result = []
    data_zone = data['data_zone']
    urls = data['urls'] 
    sleep(20)
    result.append(command.conf_begin_http_cl())
    ffi_insert_conf = cluster_master.insert_config_zone(data_zone, data['nm_config'])
    result.append(ffi_insert_conf)
    ffi_master = cluster_master.master_create_json_master(data_zone, data['nm_config'])
    result.append(ffi_master)
    ffi_notify = None
    ffi_notify = cluster_master.master_create_json_notify(data_zone, data['nm_config'], urls)
    for i_not in ffi_notify:
        result.append(i_not)
    ffi_acl = None
    ffi_acl = cluster_master.master_create_json_acl(data_zone, data['nm_config'], urls)
    for i_ac in ffi_acl:
        result.append(i_ac)
    ffi_set_files = cluster_master.set_file_all(data_zone)
    result.append(ffi_set_files)
    ffi_set_module = cluster_master.set_mods_stats_all(data_zone, "mod-stats/default")
    result.append(ffi_set_module)
    ffi_serial_policy = cluster_master.set_serial_policy_all(data_zone, "dateserial")
    result.append(ffi_serial_policy)
    result.append(command.conf_commit_http_cl())
    data_res = utils.send_http_clusters(urls, result)
    respons.append({
        "config": data['nm_config'],
        "nm_server": data['nm_master'],
        "data": data_res
    })
    return respons