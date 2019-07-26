from app import celery
from celery.result import AsyncResult
from app.libs import utils
from app.helpers import command
from app.models import model


@celery.task(bind=True)
def get_cluster_refresh_master(self, id_refresh):
    report = AsyncResult(id=id_refresh, app=refresh_zone_master)
    return report

@celery.task(bind=True)
def get_cluster_refresh_slave(self, id_refresh):
    report = AsyncResult(id=id_refresh, app=refresh_zone_slave)
    return report

@celery.task(bind=True)
def refresh_zone_master(self, id_master=None):
    if id_master is not None:
        try:
            master_data = model.get_by_id("cs_master", "id_master", id_master)[0]
        except Exception as e:
            raise e
        else:
            url_fix= "http://"+master_data['ip_master']+":"+master_data['port']
            master_server_url = url_fix+"/api/command_rest"
            json_command = command.syncronize_zone()
            response = utils.send_http(master_server_url, json_command)
            return response['data']
    else:
        try:
            master_data = model.get_all("cs_master")
        except Exception as e:
            raise e
        else:
            data = list()
            for i in master_data:
                url_fix= "http://"+i['ip_master']+":"+i['port']
                master_server_url = url_fix+"/api/command_rest"
                json_command = command.syncronize_zone()
                response = utils.send_http(master_server_url, json_command)
                data.append(response['data'])
            return data
    

@celery.task(bind=True)
def refresh_zone_slave(self, id_slave):
    if id_slave is not None:
        try:
            slave_data = model.get_by_id("v_cs_slave_node", "id_slave_node", id_slave)[0]
        except Exception as e:
            raise e
        else:
            data = list()
            url_fix= "http://"+slave_data['ip_slave_node']+":"+slave_data['port_slave_node']
            slave_server_url = url_fix+"/api/command_rest"
            json_command = command.syncronize_zone()
            response = utils.send_http(slave_server_url, json_command)
            return response['data']
    else:
        try:
            slave_data = model.get_all("cs_slave_node")
        except Exception as e:
            raise e
        else:
            data = list()
            for a in slave_data:
                url_fix= "http://"+a['ip_slave_node']+":"+a['port_slave_node']
                slave_server_url = url_fix+"/api/command_rest"
                json_command = command.syncronize_zone()
                response = utils.send_http(slave_server_url, json_command)
                data.append(response)
            return data