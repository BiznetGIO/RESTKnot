import os
from flask_script import Manager, Server
from app import socketio, app

manager = Manager(app)

manager.add_command('server', Server(host=os.getenv('APP_HOST', 'localhost'),
                                     port=int(os.getenv('APP_PORT', 5000))))

manager.add_command("socket", socketio.run(
                                app,
                                host=os.getenv('APP_HOST', 'localhost'),
                                port=int(os.getenv('APP_PORT', 5000)))) 

if __name__ == '__main__':
    manager.run()
