import json, os
from libs.command.libknot import control


def check_libs(libs):
    try:
        libs_value = os.system("ls /lib64/ | grep "+libs+"")
    except Exception as e:
        print(e)
    else:
        return libs_value

def load_libknot(libknot=None):
    libs = None
    try:
        libs = libknot
    except Exception as e:
        print(e)
        check_libs('libknot')
    else:
        control.load_lib(libs)

def load_control():
    ctl = control.KnotCtl()
    return ctl

def load_sock(knot_sock):
    ctl = load_control()
    try:
        ctl.connect(knot_sock)
    except Exception as e:
        print(e)

def send_block(params):
    ctl = load_control()
    try:
        ctl.send_block(**params)
    except Exception as e:
        print(e)

def receive(params):
    ctl = load_control()
    try:
        resp = ctl.receive(**params)
    except Exception as e:
        print(e)
    else:
        return resp

def receive_block():
    ctl = load_control()
    try:
        resp = ctl.receive_block()
    except Exception as e:
        print(e)
    else:
        return resp

def receive_stats():
    ctl = load_control()
    try:
        resp = ctl.receive_stats()
    except Exception as e:
        print(e)
    else:
        return resp

def send():
    ctl = load_control()
    try:
        ctl.send(control.KnotCtlType.END)
    except Exception as e:
        print(e)
    finally:
        ctl.close()
