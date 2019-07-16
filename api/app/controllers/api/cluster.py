from flask_restful import Resource
from app.helpers.rest import *
from app.middlewares.auth import login_required
from app.helpers import cluster_task


class ClusterCheckMaster(Resource):
    @login_required
    def get(self, id_master):
        try:
            chain = cluster_task.get_cluster_data_master.s(id_master)            
        except Exception as e:
            print(e)
        else:
            data = dict()
            res = chain()
            if res.ready():
                data = {
                    "task_id": res.task_id,
                    "state": res.status,
                    "result": res.result,
                }
            else:
                data = {
                    "task_id": res.task_id,
                    "state": res.state,
                }
            return response(200, data=data)

class ClusterCheckSlave(Resource):
    @login_required
    def get(self, id_slave):
        try:
            chain = cluster_task.get_cluster_data_slave.s(id_slave)            
        except Exception as e:
            print(e)
        else:
            data = dict()
            res = chain()
            if res.ready():
                data = {
                    "task_id": res.task_id,
                    "state": res.status,
                    "result": res.result,
                }
            else:
                data = {
                    "task_id": res.task_id,
                    "state": res.state,
                }
            return response(200, data=data)


class ClusterUnsetCheckMaster(Resource):
    @login_required
    def get(self, id_master):
        try:
            chain = cluster_task.get_cluster_data_master_unset.s(id_master)            
        except Exception as e:
            print(e)
        else:
            data = dict()
            res = chain()
            if res.ready():
                data = {
                    "task_id": res.task_id,
                    "state": res.status,
                    "result": res.result,
                }
            else:
                data = {
                    "task_id": res.task_id,
                    "state": res.state,
                }
            return response(200, data=data)

class ClusterUnsetCheckSlave(Resource):
    @login_required
    def get(self, id_slave):
        try:
            chain = cluster_task.get_cluster_data_slave_unset.s(id_slave)            
        except Exception as e:
            print(e)
        else:
            data = dict()
            res = chain()
            if res.ready():
                data = {
                    "task_id": res.task_id,
                    "state": res.status,
                    "result": res.result,
                }
            else:
                data = {
                    "task_id": res.task_id,
                    "state": res.state,
                }
            return response(200, data=data)