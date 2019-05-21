import os
import tqdm
import time
from tqdm import tqdm
from .base import Base
from libs import utils as util
from libs.listing import check_zone_authorization,list_dns, listing_endpoint
from libs import config as app
from tabulate import tabulate

class Create(Base):
    """
    usage:
        create dns (--nm=NAME) 
        create record (--nm NAME) (--nm-zn ZONENAME) (--type=TYPE) (--ttl TTL) (--nm-con CON) [--nm-con-ser CONSER] 
        create record -f FILENAME
        create record
        
        create  -h | --help

    Options :
    -h --help                 Print usage
    --nm NAME                 Set DNS/record name
    -type=TYPE                Set DNS type
    --ttl TTL                 Set DNS TTL 
    --nm-zn ZONENAME          Set zone of new record
    --nm-con CON              Set content name
    --nm-con-ser CONSER       Set content serial name
    -f FILENAME               Create Record using YAML

    Commands:
     dns                        Create DNS
     record                     Create record  
    """
    
    #@login_required
    def execute(self):
        if self.args['dns']:
            
            check = util.check_existence('zone',self.args['--nm'])
            if check['status']:
                print("ZONE ALREADY EXIST")
            else :
                if 'expired' in check['message']:
                    print(check['message'])
                else :
                    app.setDefaultDns(self.args['--nm'])

        elif self.args['record'] :
            if not self.args['--nm'] and not self.args["-f"] :
                dns = list_dns()
                if 'data' not in dns:
                    print("You don't have any dns!")
                else:
                    dns = dns['data']
                    util.convert(dns)
                    show = list()
                    for row in dns:
                        show.append({"DNS NAME" : row})
                    print("Your Domain List are ")
                    print(tabulate(show,headers='keys',showindex='always',tablefmt="rst"))
                    print("Pick a zone for your record!")
                    value = input("Zone Name : ")
                    while value not in dns:
                        print("You are not authorized to access {}, or it doesn't exist!".format(value))
                        value = input("Zone Name : ")
                    self.args['--nm-zn'] = value
                    value = input("Record name : ")
                    while not value:
                        print("Record name can't be empty string")
                        value = input("Record name : ")
                    self.args['--nm'] = value
                    print("Choose Record Type")
                    rectype = listing_endpoint('type')
                    rectype = rectype.replace('SOA\t','')
                    rectype = rectype.replace('NS\t','')
                    print(rectype)
                    rectype = rectype.split('\t')
                    del rectype[-1]
                    value = input("Record type : ")
                    while value.upper() not in rectype:
                        print("Type doesn't exist")
                        value = input("")
                    self.args['--type'] = value.upper()
                    ttl = listing_endpoint('ttl')
                    print("Available TTL values are :")
                    print(ttl)
                    ttl = ttl.split('\t')
                    del ttl[-1]
                    value = input("TTL : ")
                    while value not in ttl:
                        print("TTL value doesn't exist")
                        value = input("TTL : ")
                    self.args['--ttl'] = value
                    value = input("Content data : ")
                    while not value :
                        print("Content data can not be empty ")
                        value = input("Content data : ")
                    self.args['--nm-con'] = value
                    if self.args['--type'] == 'MX' or self.args['--type'] == 'SRV':
                        value = input("Content serial data : ")
                        while not value :
                            print("Content serial data can not be empty ")
                            value = input("Content serial data : ")
                        self.args['--nm-con-ser'] = value
                    print("You are about to create new record with following details :")
                    if self.args['--nm-con-ser']:
                        print("""Record Name : {}       Zone : {}       Type : {}       TTL : {}
Content data : {}       Content serial data :{}""".format(self.args['--nm'],self.args['--nm-zn'], self.args['--type'],self.args['--ttl'], self.args['--nm-con'],self.args['--nm-con-ser']))
                    else :
                        print("""Record Name : {}       Zone : {}       Type : {}       TTL : {}
Content data : {}      """.format(self.args['--nm'],self.args['--nm-zn'], self.args['--type'],self.args['--ttl'], self.args['--nm-con']))
                    affirm = input("Are you sure ? (Y)")
                    if affirm.upper() == 'Y':
                        self.args['--date'] = util.get_time()
                        app.setRecord(self.args)
                    else : 
                        print("Cancelled")
                        exit()

            elif self.args['--nm'] and not self.args['-f']:
                check = dict()
                skip = False
                nodata = ' '
                temp = check_zone_authorization([self.args['--nm-zn']])
                check['zone'] = temp['status']
                temp = util.check_existence('type',self.args['--type'].upper())
                check['type'] = temp['status']
                temp = util.check_existence('ttl',self.args['--ttl'])
                check['ttl'] = temp['status']

                if self.args['--type'].upper() == 'MX' or self.args['--type'].upper() == 'SRV':
                    if self.args['--nm-con-ser'] is None:
                        util.log_warning("Record {} require serial content data".format(self.args['--type'].upper()))
                        exit()
                for i in check:
                    if not check[i] :
                        nodata = nodata + i + ', '
                        skip = True
                
                if skip is True:
                    print("Value of " + nodata + "doesn't exist. \nTry command ls to check available values")
                else: 
                    self.args['--date'] = util.get_time()
                    app.setRecord(self.args)
            elif self.args['-f']:
                path = self.args['-f']
                pbar = tqdm(total=100)
                step = (100/3)
                pbar.set_description("Loading YAML")
                data = app.load_yaml(path)
                dnslist = list(data['data'].keys())
                check = check_zone_authorization(dnslist)
                sendlist = list()
                pbar.update(step)
                pbar.set_description("Parsing YAML")
                if 'data' not in check:
                    sendlist = dnslist
                    pbar.update(step)
                    
                else :
                    for i in dnslist:
                        pbar.update(step/(len(dnslist)))
                        if i not in check['data']:
                            sendlist.append(i)
                pct = (100/3)
                if sendlist:
                    print(str(sendlist) + " doesn't exist. Do you want to create these dns and continue? (Y/N)")
                    if util.assurance():
                        for i in sendlist:
                            pbar.set_description("Creating DNS {}".format(i))
                            app.setDefaultDns(i)
                            pbar.update(pct/(3*len(sendlist)))
                        pct = (100/4)
                    else :
                        print("ABORT")
                        exit()


                data = app.parse_yaml(data['data'])
                send = data['data']
                print(tabulate(send, headers="keys",tablefmt="rst" ))
                print("Create records above ? (Y) ")
                if util.assurance():
                    pbar.set_description(" Creating Record")
                    for row in send:
                        pbar.set_description(desc="Creating " + row['--nm-zn']+" "+row['--nm']+ " "+row['--type'] )
                        pbar.update(pct/(len(send)))
                        res=app.setRecord(row)
                    pbar.close()
                    print('\n')
                else :
                        print("ABORT")
                        exit()
            
        