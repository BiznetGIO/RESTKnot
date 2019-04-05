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
        cl_default.sync_conf_insert(url_ip, i_cs['id_zone'])

    record_share = list()
    column_record = model.get_columns("v_share_zone_record")
    query = "select * from v_share_zone_record where id_zone='"+fields+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record_share.append(dict(zip(column_record, row)))

    for i in record_share:
        if i['nm_type'] == 'SOA':
            url_ip = "http://"+i['ip_slave']+":"+i['port_slave']+"/api/command_rest"
            id_zone = str(i['id_zone'])
            data_soa = cl_default.sync_soa(url_ip, id_zone)
            json_command.append(data_soa)
        if i['nm_type'] == 'NS':
            url_ip = "http://"+i['ip_slave']+":"+i['port_slave']+"/api/command_rest"
            id_zone = str(i['id_zone'])
            data_ns = cl_default.sync_ns(url_ip, id_zone)
            json_command.append(data_ns)
        if i['nm_type'] == 'CNAME':
            url_ip = "http://"+i['ip_slave']+":"+i['port_slave']+"/api/command_rest"
            id_zone = str(i['id_zone'])
            id_record = str(i['id_record'])
            data_cname = cl_default.sync_cname_default(url_ip, id_zone, id_record)
            json_command.append(data_cname)
    return json_command