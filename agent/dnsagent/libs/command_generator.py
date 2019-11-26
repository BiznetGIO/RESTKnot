def conf_command(zone=None):
    begin_command = {
        "command-begin": {
            "sendblock": {
                "cmd": "conf-begin",
                "item": "domain",
                "section": "zone",
                "data": zone,
            },
            "receive": {"type": "block"},
        }
    }
    commit_command = {
        "command-commit": {
            "sendblock": {
                "cmd": "conf-commit",
                "item": "domain",
                "section": "zone",
                "data": zone,
            },
            "receive": {"type": "block"},
        }
    }
    set_command = {
        "command-set": {
            "sendblock": {
                "cmd": "conf-set",
                "item": "domain",
                "section": "zone",
                "data": zone,
            },
            "receive": {"type": "block"},
        }
    }
    return begin_command, commit_command, set_command


def zone_command(zone=None):
    begin_command = {
        "zone-begin": {
            "sendblock": {"cmd": "zone-begin", "zone": zone, "data": zone},
            "receive": {"type": "block"},
        }
    }
    commit_command = {
        "zone-commit": {
            "sendblock": {"cmd": "zone-commit", "zone": zone, "data": zone},
            "receive": {"type": "block"},
        }
    }
    return begin_command, commit_command


def file_set_command(zone, id_zone):
    fileset_command = {
        "file-set": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "file",
                "identifier": zone,
                "section": "zone",
                "data": str(id_zone) + "_" + zone + ".zone",
            },
            "receive": {"type": "block"},
        }
    }
    return fileset_command


def set_master_command(zone, nm_master):
    master_command = {
        "slave-set-master": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "master",
                "section": "zone",
                "data": nm_master,
            },
            "receive": {"type": "block"},
        }
    }
    return master_command


def acl_command(zone, nm_master):
    command = {
        "slave-set-notify": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "acl",
                "section": "zone",
                "data": nm_master,
            },
            "receive": {"type": "block"},
        }
    }
    return command


def modstat_set(zone, value):
    command = {
        "modstat-set": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "module",
                "section": "zone",
                "data": value,
            },
            "receive": {"type": "block"},
        }
    }
    return command


def set_serial(zone, value):
    command = {
        "serial-set": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "serial-policy",
                "section": "zone",
                "data": value,
            },
            "receive": {"type": "block"},
        }
    }
    return command


def notify_command(zone, nm_master):
    command = {
        "slave-set-notify": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "notify",
                "section": "zone",
                "data": nm_master,
            },
            "receive": {"type": "block"},
        }
    }
    return command
