from app.libs import utils
from app.models import model as model
from app import db
from app.libs import utils
from . import cl_default


def cluster_zone(tags):
    # Get Zone
    json_command = list()
    fields = tags['id_zone']
    record_cs = list()
    column_record = model.get_columns("v_cs_acl_slave")
    query = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record_cs.append(dict(zip(column_record, row)))
    for i_cs in record_cs:
        url_ip = "http://"+i_cs['ip_slave']+":"+i_cs['port_slave']+"/api/command_rest"
        print(url_ip)
        conf_insert = cl_default.sync_conf_insert(url_ip, i_cs['id_zone'])
        json_command.append(conf_insert)
    return json_command

def unset_cluster(tags):
    # Get Zone
    json_command = list()
    fields = tags['id_zone']
    record_cs = list()
    column_record = model.get_columns("v_cs_acl_slave")
    query = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record_cs.append(dict(zip(column_record, row)))
    for i_cs in record_cs:
        url_ip = "http://"+i_cs['ip_slave']+":"+i_cs['port_slave']+"/api/command_rest"
        conf_insert = cl_default.sync_conf_unset(url_ip, i_cs['id_zone'])
        json_command.append(conf_insert)
    return json_command

# def unset_cluster(tags):
#     json_command = list()
#     fields = tags['id_zone']
#     record_cs = list()
#     column_record = model.get_columns("v_cs_acl_slave")
#     query = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
#     db.execute(query)
#     rows = db.fetchall()
#     for row in rows:
#         record_cs.append(dict(zip(column_record, row)))
#     for i_cs in record_cs:
#         url_ip = "http://"+i_cs['ip_slave']+":"+i_cs['port_slave']+"/api/command_rest"
#         unset_conf = cl_default.sync_conf_unset(url_ip, str(i_cs['id_zone']))
#         if unset_conf['status'] == 'Command Execute':
#             data_state_acl = {
#                 "where":{
#                     "id_acl_master" : str(i_cs['id_acl_master'])
#                 },
#                 "data":{
#                     "state" : "3"
#                 }
#             }
#             record_notify=list()
#             cl_notify = model.get_columns("cs_notify_master")
#             query_notify = "SELECT * FROM cs_notify_master where id_zone='"+str(i_cs['id_zone'])+"'"
#             db.execute(query_notify)
#             rows_notify = db.fetchall()
#             for row_n in rows_notify:
#                 record_notify.append(dict(zip(cl_notify, row_n)))
#             for a in record_notify:
#                 data_state_notify = {
#                     "where":{
#                         "id_notify_master" : str(a['id_notify_master'])
#                     },
#                     "data":{
#                         "state" : "3"
#                     }
#                 }
#                 model.update("cs_notify_master", data_state_notify)
#                 model.update("cs_notify_slave", data_state_notify)
#             model.update("cs_acl_master", data_state_acl)
#             model.update("cs_acl_slave", data_state_acl)
#             # db.update("cs_notify_master", data_state_notify)
#             # db.update("cs_notify_slave", data_state_notify)
#         json_command.append(unset_conf)
#     return json_command