import os
import sys
from .base import Base
from libs import utils as util
from libs import config as app
from libs import listing as sort
from libs.wrapper import *
import string
from tabulate import tabulate

class Sync(Base):
    """
    Usage:
      sync dns
      sync record 
      sync -h | --help

    Options:
      -h --help         Print this message

    Commands:
      dns               List unsynchronized dns
      record            List unsynchronized records
    """

    def execute(self):
        if self.args['dns']:
            d_dns = sort.list_dns()
            if d_dns['status']:
                d_dns = d_dns['data']
                dat = list()
                for row in d_dns:
                    tmp = sort.get_data('zone',key=None,tags='nm_zone',value=row)['data'][0]
                    dat.append(tmp)
                d_unsync = list()
                d_id = list()
                for row in dat:
                    if row['state'] == 0:
                        d_unsync.append(row)
                        d_id.append(row['id_zone'])
                if d_unsync:
                    print("\n============================ Unsynchronized DNS ============================\n")
                    d_unsync = util.convert(d_unsync)
                    d_unsync = util.table_cleanup(d_unsync)
                    print(tabulate(d_unsync,headers='keys',showindex='always',tablefmt="rst"))
                    index = input("""
Type the index of the zone (0~{}), if you want to remove multiple record
separate the index using comma (,)
""".format(len(d_id)-1))
                    index = index.split(',')
                    index = util.check_availability(index,(len(d_id)-1))
                    for idx in index:
                        d_sync = { "sync" : "dns", "data" : {"id_zone" : d_id[int(idx)] } }
                        res=app.syncdat(d_sync)
                else :
                    print("All dns is already synchronized with knot server")            
        elif self.args['record']:
            zone = sort.list_dns()
            zone = zone['data']
            show = sort.list_record(zone)
            show = show['data']
            d_record = list()
            id_record = list()
            for row in show:
                if row['state'] == 0:
                    id_record.append(row['id_record'])
                    d_record.append(row)
            if len(d_record)<=0 :
                print("All record is already synchronized with Knot server")
                return 0
            else :
                d_record = util.table_cleanup(d_record)
                print(tabulate(d_record,headers="keys",showindex="always",tablefmt="rst"))
                index = input("""
    Type the index of the record (0~{}), if you want to remove multiple record
    separate the index using comma (,)
    """.format(len(d_record)-1))
                index = index.split(',')
                index = util.check_availability(index,(len(show)-1))
                for idx in index:
                    d_sync = {"sync" : "record", "data" : {"id_record" : id_record[int(idx)]}}
                    res=app.syncdat(d_sync)
                    if not res["status"]:
                        sys.stderr.write("Failure on index {}".format(idx))                 