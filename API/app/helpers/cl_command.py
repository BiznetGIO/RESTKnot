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
        conf_insert = cl_default.sync_conf_insert(url_ip, i_cs['id_zone'])
        json_command.append(conf_insert)
    return json_command